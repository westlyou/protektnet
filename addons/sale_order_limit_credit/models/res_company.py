# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    credit_days_limit = fields.Integer(
        string='Credit Days Limit',
    )
