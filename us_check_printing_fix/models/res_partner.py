# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_account_number = fields.Char(
        string='Account Number',
        help='Account number for this partner, printed on checks in the memo field.',
    )
