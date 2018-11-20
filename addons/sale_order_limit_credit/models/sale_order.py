# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    blocked_client = fields.Char(
        string='Message Credit Limit',
        compute="_compute_blocked_client"
    )

    @api.depends('partner_id')
    def _compute_blocked_client(self):
        invoice_due = self.env['account.invoice'].search([
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'open')])
        amount_credit = sum(invoice_due.mapped('residual'))
        days_passed = [(fields.Date.from_string(
            fields.Date.today()) - fields.Date.from_string(date)
        ).days for date in invoice_due.mapped('date_due')]
        days_company = self.company_id.credit_days_limit
        days_partner = self.partner_id.credit_days_limit
        days_limit = (
            days_company if days_company == days_partner else days_partner)
        dates = any(day > days_limit for day in days_passed)
        if self.partner_id.credit_limit < amount_credit or dates:
            self.blocked_client = True
