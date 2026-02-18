from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_profit = fields.Monetary(
        string='Total Profit (Lifetime)',
        compute='_compute_profitability_stats',
        currency_field='currency_id',
        groups='account.group_account_manager',
        help='Total profit from all posted customer invoices and credit notes'
    )
    
    avg_profit_per_sale = fields.Monetary(
        string='Avg Profit Per Sale',
        compute='_compute_profitability_stats',
        currency_field='currency_id',
        groups='account.group_account_manager',
        help='Average profit per customer invoice (excludes credit notes from calculation)'
    )
    
    invoice_count_for_profit = fields.Integer(
        string='Sales Count',
        compute='_compute_profitability_stats',
        groups='account.group_account_manager',
        help='Number of posted customer invoices (used for average calculation)'
    )

    @api.depends('invoice_ids.invoice_profit', 'invoice_ids.state', 'invoice_ids.move_type')
    def _compute_profitability_stats(self):
        """
        Calculate lifetime profit statistics for this partner.
        
        Total Profit = sum of invoice_profit for all posted invoices + credits
        Avg Per Sale = sum of invoice_profit for invoices only / count of invoices
        
        Credit notes are INCLUDED in total profit (they reduce it)
        Credit notes are EXCLUDED from average calculation (avoids skewing)
        """
        for partner in self:
            # Get all posted customer invoices and credit notes
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('state', '=', 'posted')
            ])
            
            # Total profit: all transactions (invoices + credits)
            total = sum(invoices.mapped('invoice_profit'))
            
            # Average profit per sale: only invoices (exclude credits)
            sales = invoices.filtered(lambda m: m.move_type == 'out_invoice')
            sales_count = len(sales)
            avg = sum(sales.mapped('invoice_profit')) / sales_count if sales_count else 0.0
            
            partner.total_profit = total
            partner.avg_profit_per_sale = avg
            partner.invoice_count_for_profit = sales_count
