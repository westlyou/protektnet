# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_days_limit = fields.Integer(
        string='Credit Days Limit',
        default=lambda self: self.env.user.company_id.credit_days_limit
    )
    credit_limit = fields.Integer(string="Credit Limit")
    credit_on_hold = fields.Boolean(string="Put on Hold")
    bool_credit_limit = fields.Boolean(
        string='Credit Limit',
        compute="_compute_bool_credit_limit",
    )

    def _compute_bool_credit_limit(self):
        self.bool_credit_limit = self.env.user.has_group(
            'sale_order_limit_credit.group_credit_limit')
