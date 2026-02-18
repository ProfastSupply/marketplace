from odoo import api, fields, models
from datetime import timedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_cost = fields.Monetary(
        string='Cost',
        compute='_compute_invoice_profitability',
        store=True,
        readonly=True,
        groups='account.group_account_manager',
        help='Total cost of goods sold (COGS) based on product standard prices at invoice time'
    )
    
    invoice_profit = fields.Monetary(
        string='Profit',
        compute='_compute_invoice_profitability',
        store=True,
        readonly=True,
        groups='account.group_account_manager',
        help='Revenue minus cost. Frozen after 7 days to preserve historical accuracy.'
    )

    @api.depends(
        'invoice_line_ids.product_id',
        'invoice_line_ids.quantity',
        'amount_untaxed',
        'move_type',
        'invoice_date'
    )
    def _compute_invoice_profitability(self):
        """
        Calculate cost and profit for customer invoices.
        
        Cost = sum(product.standard_price * quantity) for each line
        Profit = amount_untaxed - cost
        
        IMPORTANT: Only recalculates if invoice_date is within the last 7 days
        or if invoice_date is not set. This preserves historical accuracy when
        product costs change over time.
        
        EXCEPTION: On module install, the post_init_hook sets context flag
        'force_compute_profitability' to compute ALL invoices once.
        
        Only applies to out_invoice and out_refund move types.
        """
        today = fields.Date.context_today(self)
        cutoff_date = today - timedelta(days=7)
        
        for record in self:
            # Only compute for customer invoices and credit notes
            if record.move_type not in ('out_invoice', 'out_refund'):
                record.invoice_cost = 0.0
                record.invoice_profit = 0.0
                continue
            
            # Skip freeze check if called from post_init_hook
            if not self.env.context.get('force_compute_profitability'):
                # FREEZE historical invoices (>7 days old)
                # This prevents retroactive changes when product costs are updated
                if record.invoice_date and record.invoice_date < cutoff_date:
                    # Don't recalculate - preserve historical values
                    continue
            
            # Calculate cost from invoice lines
            cost = 0.0
            for line in record.invoice_line_ids:
                product = line.product_id
                quantity = line.quantity or 0.0
                
                if not product:
                    continue
                
                # For customer invoices: add COGS
                if record.move_type == 'out_invoice':
                    line_cost = (product.standard_price or 0.0) * quantity
                    cost += line_cost
                
                # For credit notes: cost is typically not tracked
                # (treating as pure revenue reduction)
                elif record.move_type == 'out_refund':
                    # Optional: uncomment next line if you want to track
                    # returned goods cost
                    # line_cost = (product.standard_price or 0.0) * quantity
                    # cost += line_cost
                    pass
            
            # Calculate profit
            profit = 0.0
            if record.move_type == 'out_invoice':
                profit = record.amount_untaxed - cost
            elif record.move_type == 'out_refund':
                # Credit notes reduce revenue (negative profit impact)
                profit = -record.amount_untaxed
            
            record.invoice_cost = cost
            record.invoice_profit = profit
