# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    change_user_id = fields.Boolean(
        string='Change SalePerson',
        compute='_compute_change_user_id',
    )

    def _compute_change_user_id(self):
        self.change_user_id = self.env.user.has_group(
            'customs_grupo_censere.group_sales_person')
