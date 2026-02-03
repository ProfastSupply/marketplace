# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_po_origin = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        readonly=True,
        copy=False,
    )

    def action_create_invoice(self):
        """Create invoice from the related sale order."""
        self.ensure_one()
        
        # Get the related sale order
        sale_order = self.sale_id
        if not sale_order:
            raise UserError(_("No sales order linked to this delivery."))
        
        # Check if there's anything to invoice
        if sale_order.invoice_status != 'to invoice':
            raise UserError(_("Nothing to invoice on this sales order."))
        
        # Create the invoice using Odoo's standard method
        invoice = sale_order._create_invoices()
        
        if not invoice:
            raise UserError(_("Could not create invoice."))
        
        # Open the created invoice
        return {
            'name': _('Customer Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    def _compute_po_origin(self):
        """Find and set the related purchase order based on group_id."""
        for picking in self:
            if picking.sale_id or picking.x_po_origin:
                # Skip if already has sale order or PO already set
                continue
            
            if not picking.group_id:
                continue
                
            # Check if group name starts with 'P' (purchase order reference)
            group_name = picking.group_id.name or ''
            if not group_name.startswith('P'):
                continue
            
            # Search for matching purchase order
            po = self.env['purchase.order'].search([
                ('name', '=', group_name)
            ], limit=1)
            
            if po:
                picking.x_po_origin = po.id

    def write(self, vals):
        res = super().write(vals)

        pickings_to_compute = self.filtered(
            lambda p:
                not p.x_po_origin
                and not p.sale_id
                and p.group_id
        )

        pickings_to_compute._compute_po_origin()

        return res


    @api.model_create_multi
    def create(self, vals_list):
        """Compute PO origin on create if needed."""
        pickings = super().create(vals_list)
        
        pickings_to_compute = pickings.filtered(
            lambda p: not p.sale_id and not p.x_po_origin and p.group_id
        )
        pickings_to_compute._compute_po_origin()
        
        return pickings
