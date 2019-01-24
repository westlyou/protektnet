# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#    Part of Odoo. See LICENSE file for full copyright and licensing details.   #
#    Copyright (C) 2018 Jupical Technologies Pvt. Ltd. <http://www.jupical.com> #
#                                                                               #
#################################################################################

from odoo import fields, models, api

class Mail(models.Model):

    _inherit = "mail.mail"

    @api.model
    def create(self, vals):
        active_company_id = self.env.user.company_id and self.env.user.company_id.id
        out_mail_sever = self.env['ir.mail_server'].search([('company_id', '=', active_company_id)])
        if out_mail_sever and not self._context.get('cron_server', False):
            vals.update({'mail_server_id':out_mail_sever.id})

        result = super(Mail, self).create(vals)
        return result

class MailMessage(models.Model):

    _inherit = "mail.message"

    @api.model
    def create(self, vals):
        active_company_id = self.env.user.company_id and self.env.user.company_id.id
        out_mail_sever = self.env['ir.mail_server'].search([('company_id', '=', active_company_id)])
        if out_mail_sever and not self._context.get('cron_server', False):
            vals.update({'mail_server_id':out_mail_sever.id})

        result = super(MailMessage, self).create(vals)
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:





