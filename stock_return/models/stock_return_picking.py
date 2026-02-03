# -*- coding: utf-8 -*-

from odoo import models


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def action_return_max_quantities(self):
        """Set all line quantities to max and process the return."""
        self.ensure_one()
        
        # Set each line's quantity to the max delivered quantity
        for line in self.product_return_moves:
            line.quantity = line.move_quantity
        
        # Call the standard return method and return its action
        return self.action_create_returns()
