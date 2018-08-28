from odoo import api, fields, models

class XCustomMailGatewayComposer(models.TransientModel):
    """
        Update email_from field in composer box
    """

    _inherit = 'mail.compose.message'

    @api.onchange('mail_server_id')
    def onchange_mail_server_id(self):
        self.update({
        	'email_from': '%s <%s>' % (self.env['res.users'].browse(self.env.uid).name, self.mail_server_id.smtp_user),
        	'reply_to': self.mail_server_id.smtp_user,
        })
