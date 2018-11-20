# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_days_limit = fields.Integer(
        string='Credit Days Limit',
        default=lambda self: self.env.user.company_id.credit_days_limit
    )
