# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_regenerate_invoice_lines(self):
        """
        Regenerate invoice lines from sale order lines that are still to invoice.
        Keeps the current record, deletes other draft invoices for the same order,
        and rebuilds lines from sale.order.line where invoice_status = 'to invoice'.
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

        # If there are multiple invoices, ensure all are draft
        if len(all_invoices) > 1:
            if any(inv.state != 'draft' for inv in all_invoices):
                raise UserError(_("Cannot consolidate: there are posted invoices for this order."))

            # Delete all other invoices EXCEPT the current one
            invoices_to_delete = all_invoices - record
            if invoices_to_delete:
                invoices_to_delete.sudo().unlink()

        # Delete existing invoice lines on THIS record
        record.invoice_line_ids.sudo().unlink()

        # Get related sale order
        sale_order = self.env['sale.order'].search([
            ('name', '=', record.invoice_origin)
        ], limit=1)

        if not sale_order:
            raise UserError(_("Related sales order not found."))

        # Build invoice lines from lines that still need invoicing
        new_lines = []
        total_amount = 0.0

        for line in sale_order.order_line:
            # Skip sections/notes
            if line.display_type:
                continue

            # Only lines that still need invoicing
            if line.invoice_status != 'to invoice':
                continue

            qty = line.qty_to_invoice

            line_total = qty * line.price_unit * (1 - line.discount / 100)
            total_amount += line_total

            new_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_ids': [(6, 0, line.tax_id.ids)],
                'product_uom_id': line.product_uom.id,
                'sale_line_ids': [(6, 0, [line.id])],
            }))

        if not new_lines:
            raise UserError(_("No sale order lines found that are ready to be invoiced."))

        record.write({'invoice_line_ids': new_lines})

        # Switch invoice type if necessary based on total
        if total_amount < 0 and record.move_type == 'out_invoice':
            record.sudo().action_switch_move_type()
        elif total_amount >= 0 and record.move_type == 'out_refund':
            record.sudo().action_switch_move_type()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': record.id,
            'target': 'current',
        }
