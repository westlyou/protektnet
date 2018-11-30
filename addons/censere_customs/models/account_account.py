# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'account.account'

    tag_names = fields.Char(
        string='Tags',
        compute='_compute_tag_names'
    )

    @api.depends('tag_ids')
    def _compute_tag_names(self):
        for rec in self:
            rec.tag_names = ('/').join([tag.name for tag in rec.tag_ids])
