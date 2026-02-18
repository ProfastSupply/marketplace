# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # -- Many2many approvers --------------------------------------------------
    # res.config.settings is a transient model -- compute/inverse is unreliable
    # for Many2many because the relation table gets wiped between sessions.
    # The correct Odoo pattern is to override get_values/set_values and
    # serialize IDs into ir.config_parameter manually.

    credit_hold_approver_ids = fields.Many2many(
        comodel_name='res.users',
        relation='credit_hold_config_approver_rel',
        column1='config_id',
        column2='user_id',
        string='Credit Hold Approvers',
        help='Any of these users can approve a Sale Order blocked by a credit hold. '
             'All of them receive an activity when a new blocked order needs attention.',
    )

    # -- Single notification recipient ----------------------------------------
    credit_hold_notify_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Credit Hold Notification Recipient',
        help='This person receives activities when a customer is automatically '
             'placed on hold or released. Separate from the approvers who action '
             'blocked Sale Orders.',
    )

    # -- Persistence via ir.config_parameter ---------------------------------

    def get_values(self):
        res = super().get_values()
        ICP = self.env['ir.config_parameter'].sudo()

        param = ICP.get_param('credit_hold.approver_user_ids', '')
        user_ids = [int(x) for x in param.split(',') if x.strip().isdigit()]
        res['credit_hold_approver_ids'] = [(6, 0, user_ids)]

        notify_param = ICP.get_param('credit_hold.notify_user_id', '')
        res['credit_hold_notify_user_id'] = int(notify_param) if notify_param.isdigit() else False

        return res

    def set_values(self):
        super().set_values()
        ICP = self.env['ir.config_parameter'].sudo()

        ICP.set_param(
            'credit_hold.approver_user_ids',
            ','.join(str(uid) for uid in self.credit_hold_approver_ids.ids),
        )
        ICP.set_param(
            'credit_hold.notify_user_id',
            str(self.credit_hold_notify_user_id.id) if self.credit_hold_notify_user_id else '',
        )

        # Keep the studio approval rule in sync with whatever is configured here
        rule = self.env.ref(
            'credit_hold.credit_hold_so_approval_rule', raise_if_not_found=False
        )
        if rule:
            notify_ids = (
                [self.credit_hold_notify_user_id.id]
                if self.credit_hold_notify_user_id
                else []
            )
            rule.sudo().write({
                'approver_ids': [(6, 0, self.credit_hold_approver_ids.ids)],
                'users_to_notify': [(6, 0, notify_ids)],
            })

