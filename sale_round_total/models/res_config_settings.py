from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_rounding_increment = fields.Selection(
        selection=[
            ('0.05', '5¢  (Nickel)'),
            ('0.25', '25¢ (Quarter)'),
            ('1.00', '$1.00'),
        ],
        string='Rounding Increment',
        default='0.05',
        help='Nearest increment to which the sale order after-tax total will be rounded.',
    )

    sale_rounding_direction = fields.Selection(
        selection=[
            ('up',      'Round Up Only'),
            ('nearest', 'Round to Nearest'),
            ('down',    'Round Down Only'),
        ],
        string='Rounding Direction',
        default='up',
        help=(
            'Round Up Only: always round to the next increment (total never decreases).\n'
            'Round to Nearest: round to whichever increment boundary is closer.\n'
            'Round Down Only: always round to the previous increment (total never increases).'
        ),
    )

    # ------------------------------------------------------------------
    # Explicitly manage params so Odoo never DELETES the record on False.
    # Using set_values/get_values instead of config_parameter= on the
    # field keeps the ir.config_parameter record alive at all times.
    # ------------------------------------------------------------------

    def set_values(self):
        super().set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('sale_rounding.increment',  self.sale_rounding_increment or '0.05')
        ICP.set_param('sale_rounding.direction',  self.sale_rounding_direction or 'up')

    # Valid selection keys — used to normalize whatever float string
    # ir.config_parameter returns (e.g. '1.0' → '1.00').
    _VALID_INCREMENTS = {'0.05', '0.25', '1.00'}
    _INCREMENT_NORMALIZE = {
        '0.05': '0.05',
        '.05':  '0.05',
        '0.25': '0.25',
        '.25':  '0.25',
        '1.0':  '1.00',
        '1':    '1.00',
        '1.00': '1.00',
    }

    @api.model
    def get_values(self):
        res = super().get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        raw = ICP.get_param('sale_rounding.increment', '0.05')
        increment = self._INCREMENT_NORMALIZE.get(raw, raw)
        if increment not in self._VALID_INCREMENTS:
            increment = '0.05'
        # Write the normalized value back so it doesn't cause errors next time
        if raw != increment:
            ICP.set_param('sale_rounding.increment', increment)
        res['sale_rounding_increment'] = increment

        # Migration: if the old up_only param exists and new direction param
        # does not, convert automatically so existing installs don't reset.
        direction = ICP.get_param('sale_rounding.direction', '')
        if not direction:
            old_up_only = ICP.get_param('sale_rounding.up_only', 'True')
            direction = 'up' if old_up_only in ('True', '1', 'true') else 'nearest'
            ICP.set_param('sale_rounding.direction', direction)

        res['sale_rounding_direction'] = direction
        return res
