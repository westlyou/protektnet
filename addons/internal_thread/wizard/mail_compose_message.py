# -*- coding: utf-8 -*-

from odoo import api, fields, models


class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    send_only_internal = fields.Boolean(
        string="Send private",
        help="The message will be sent only for recipients below. It will not be sent to documents followers",
    )

    @api.multi
    def send_mail(self, auto_commit=False):
        res = False
        for wizard in self:
            if wizard.send_only_internal:
                res = super(mail_compose_message, self.with_context(
                    put_this_subtype_instead='internal_thread.mt_internal_mes',
                )).send_mail(auto_commit=auto_commit)
        return res if res else super(mail_compose_message, self).send_mail(auto_commit=auto_commit)
