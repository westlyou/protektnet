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

from odoo import fields, models
import threading
import logging
_logger = logging.getLogger(__name__)


class MassMailing(models.Model):

    _inherit = 'mail.mass_mailing'

    outgoing_mail_server = fields.Many2one(
        "ir.mail_server", string="Outgoing Mail Server", help="Select an outgoing mail server that you want to use for this mass mailing.")

    def send_mail(self):
        author_id = self.env.user.partner_id.id
        outgoing_mail_server = int(self.env['ir.config_parameter'].sudo().get_param(
            'mass_mailing_outgoing_mailserver.outgoing_mail_server'))
        for mailing in self:
            # instantiate an email composer + send emails
            res_ids = mailing.get_remaining_recipients()
            if not res_ids:
                raise UserError(_('Please select recipients.'))

            # Convert links in absolute URLs before the application of the
            # shortener
            mailing.body_html = self.env['mail.template']._replace_local_links(
                mailing.body_html)

            composer_values = {
                'author_id': author_id,
                'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
                'body': mailing.convert_links()[mailing.id],
                'subject': mailing.name,
                'model': mailing.mailing_model_real,
                'email_from': mailing.email_from,
                'record_name': False,
                'composition_mode': 'mass_mail',
                'mass_mailing_id': mailing.id,
                'mailing_list_ids': [(4, l.id) for l in mailing.contact_list_ids],
                'no_auto_thread': mailing.reply_to_mode != 'thread',
            }
            if mailing.outgoing_mail_server:
                composer_values.update(
                    {'mail_server_id': mailing.outgoing_mail_server.id})
            elif outgoing_mail_server:
                composer_values.update(
                    {'mail_server_id': outgoing_mail_server})
            if mailing.reply_to_mode == 'email':
                composer_values['reply_to'] = mailing.reply_to
            composer = self.env['mail.compose.message'].with_context(
                active_ids=res_ids).create(composer_values)
            extra_context = self._get_mass_mailing_context()
            composer = composer.with_context(active_ids=res_ids, **extra_context)
            auto_commit = not getattr(threading.currentThread(), 'testing', False)
            composer.send_mail(auto_commit=auto_commit)
            mailing.state = 'done'
        return True
