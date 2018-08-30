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


from odoo import api, fields, models, tools


class TestMassMailing(models.TransientModel):
    _inherit = 'mail.mass_mailing.test'

    @api.multi
    def send_mail_test(self):
        self.ensure_one()
        mails = self.env['mail.mail']
        mailing = self.mass_mailing_id

        outgoing_mail_server = int(self.env['ir.config_parameter'].sudo().get_param(
            'mass_mailing_outgoing_mailserver.outgoing_mail_server'))
        test_emails = tools.email_split(self.email_to)
        for test_mail in test_emails:
            # Convert links in absolute URLs before the application of the
            # shortener
            mailing.write(
                {'body_html': self.env['mail.template']._replace_local_links(mailing.body_html)})
            mail_values = {
                'email_from': mailing.email_from,
                'reply_to': mailing.reply_to,
                'email_to': test_mail,
                'subject': mailing.name,
                'body_html': mailing.body_html,
                'notification': True,
                'mailing_id': mailing.id,
                'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
            }
            if mailing.outgoing_mail_server:
                mail_values.update(
                    {'mail_server_id': mailing.outgoing_mail_server.id})
            elif outgoing_mail_server:
                mail_values.update(
                    {'mail_server_id': outgoing_mail_server})
            mail = self.env['mail.mail'].create(mail_values)
            mails |= mail
        mails.send()
        return True
