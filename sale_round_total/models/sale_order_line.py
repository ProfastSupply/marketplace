from odoo import api, fields, models

# Fields that, when changed by a user, should trigger a live rounding recompute
_ROUNDING_TRIGGER_FIELDS = {'price_unit', 'product_uom_qty', 'tax_id', 'product_id'}


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit_before_rounding = fields.Float(
        string='Price Before Rounding',
        digits='Product Price',
        default=0.0,
        copy=False,
        help='Snapshot of price_unit taken before the rounding adjustment was applied.',
    )

    # ------------------------------------------------------------------
    # Write override — triggers live recompute on relevant field changes
    # ------------------------------------------------------------------
    def write(self, vals):
        # Bail immediately if our own rounding code is writing — prevents
        # recursive recompute loops.
        if self.env.context.get('rounding_in_progress'):
            return super().write(vals)

        user_edit = bool(_ROUNDING_TRIGGER_FIELDS & set(vals.keys()))

        # If the user is manually editing price_unit on a non-draft confirmed
        # order, treat their value as the new "real" price by updating the
        # before_rounding snapshot before the recompute fires.
        if user_edit and 'price_unit' in vals:
            for line in self:
                if line.order_id.state != 'draft' and line.order_id.sale_rounding_applied:
                    super(SaleOrderLine, line.with_context(rounding_in_progress=True)).write(
                        {'price_unit_before_rounding': vals['price_unit']}
                    )

        result = super().write(vals)

        if user_edit:
            self._trigger_live_rounding()

        return result

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._trigger_live_rounding()
        return records

    def unlink(self):
        orders = self.mapped('order_id')
        result = super().unlink()
        for order in orders.exists():
            if order.state != 'draft' and order._rounding_is_live():
                order.sale_rounding_applied = False
                order._apply_rounding()
        return result

    def _trigger_live_rounding(self):
        """Recompute rounding on parent orders that qualify for live updates."""
        orders = self.mapped('order_id').filtered(
            lambda o: o.state != 'draft' and o._rounding_is_live()
        )
        for order in orders:
            order._apply_rounding()
