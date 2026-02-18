# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    credit_hold_blocked = fields.Boolean(
        string='Blocked by Credit Hold',
        compute='_compute_credit_hold_blocked',
        store=False,
    )
    credit_hold_pending = fields.Boolean(
        string='Credit Hold Approval Pending',
        compute='_compute_credit_hold_pending',
        store=False,
    )

    @api.depends('partner_id.x_account_hold')
    def _compute_credit_hold_blocked(self):
        for order in self:
            order.credit_hold_blocked = bool(order.partner_id.x_account_hold)

    @api.depends('partner_id.x_account_hold', 'activity_ids',
                 'activity_ids.activity_category')
    def _compute_credit_hold_pending(self):
        for order in self:
            order.credit_hold_pending = (
                order.partner_id.x_account_hold
                and any(
                    a.activity_category == 'grant_approval'
                    for a in order.activity_ids
                )
            )
