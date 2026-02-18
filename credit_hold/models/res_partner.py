# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_account_hold = fields.Boolean(
        string='Account On Hold',
        default=False,
        help='When enabled, new Sale Orders for this customer will require '
             'approval before they can be confirmed.',
    )
    x_credit_limit = fields.Monetary(
        string='Customer Credit Limit',
        currency_field='currency_id',
        help='When the sum of open (unpaid/partially paid) invoices exceeds '
             'this amount the account will be placed on hold automatically.',
    )
