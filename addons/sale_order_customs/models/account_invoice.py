# -*- coding: utf-8 -*-
# © <2019> <Grupo Censere>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _l10n_mx_edi_retry(self):
        invoice_po = self.invoice_line_ids.mapped('sale_line_ids').mapped(
            'order_id').mapped(
            'auto_purchase_order_id').sudo().invoice_ids.filtered(
            lambda x: x.state == 'draft')
        invoice_po.sudo().write({
            'reference': self.number,
        })
        invoice_po.sudo().action_invoice_open()
        return super(account_invoice, self)._l10n_mx_edi_retry()
