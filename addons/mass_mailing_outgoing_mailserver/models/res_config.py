# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    outgoing_mail_server = fields.Many2one(
        "ir.mail_server", string="Outgoing Mail Server", help="Outgoing mail server used for mass mailing")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            outgoing_mail_server=int(ICPSudo.get_param(
                'mass_mailing_outgoing_mailserver.outgoing_mail_server')),

        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param(
            "mass_mailing_outgoing_mailserver.outgoing_mail_server", self.outgoing_mail_server.id)
