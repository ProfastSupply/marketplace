# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_regenerate_invoice_lines(self):
        """
        Regenerate invoice lines from delivered quantities on the sale order.
        Consolidates multiple draft invoices for the same order.
        """
        self.ensure_one()
        record = self

        # Validate invoice type
        if record.move_type not in ('out_invoice', 'out_refund'):
            raise UserError(_("This action only applies to customer invoices or credit notes."))
        
        if record.state != 'draft':
            raise UserError(_("Invoice must be in draft state to regenerate lines."))
        
        if not record.invoice_origin:
            raise UserError(_("Invoice has no source document reference."))

        # Find all invoices for the same sale order (not cancelled)
        all_invoices = self.env['account.move'].search([
            ('invoice_origin', '=', record.invoice_origin),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '!=', 'cancel')
        ])

        # Handle multiple invoices - consolidate if all are drafts
        if len(all_invoices) > 1:
            # If ANY are posted, stop immediately
            if any(inv.state != 'draft' for inv in all_invoices):
                raise UserError(_("Cannot consolidate: there are posted invoices for this order."))
            
            # Keep the oldest draft (lowest ID) and delete the rest
            oldest_invoice = min(all_invoices, key=lambda inv: inv.id)
            invoices_to_delete = all_invoices - oldest_invoice
            invoices_to_delete.sudo().unlink()
            
            # Re-assign record to the survivor
            record = oldest_invoice

        # Delete existing invoice lines
        record.invoice_line_ids.sudo().unlink()

        # Get related sale order
        sale_order = self.env['sale.order'].search([
            ('name', '=', record.invoice_origin)
        ], limit=1)
        
        if not sale_order:
            raise UserError(_("Related sales order not found."))

        # Build invoice lines from delivered items
        new_lines = []
        total_amount = 0.0

        for line in sale_order.order_line:
            # Skip display-only lines (sections, notes)
            if line.display_type:
                continue
            
            delivered_qty = line.qty_delivered
            
            # Skip lines with no delivery
            if delivered_qty <= 0:
                continue
            
            # Skip products not invoiced on delivery
            if line.product_id.invoice_policy != 'delivery':
                continue

            line_total = delivered_qty * line.price_unit * (1 - line.discount / 100)
            total_amount += line_total

            new_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': delivered_qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_ids': [(6, 0, line.tax_id.ids)],
                'product_uom_id': line.product_uom.id,
                'sale_line_ids': [(6, 0, [line.id])],
            }))

        if not new_lines:
            raise UserError(_("No delivered items found to invoice."))

        record.write({'invoice_line_ids': new_lines})

        # Switch invoice type if necessary based on total
        if total_amount < 0 and record.move_type == 'out_invoice':
            record.sudo().action_switch_move_type()
        elif total_amount >= 0 and record.move_type == 'out_refund':
            record.sudo().action_switch_move_type()

        # Invert quantities if credit note
        if record.move_type == 'out_refund':
            for line in record.invoice_line_ids:
                line.write({'quantity': -line.quantity})

        # Return action to reload the form (in case we switched to a different record)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': record.id,
            'target': 'current',
        }
