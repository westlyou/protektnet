# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    total_planned = fields.Float(
        compute="_compute_total_planned",
        store=True,)

    @api.multi
    @api.depends('task_ids')
    def _compute_total_planned(self):
        for rec in self:
            rec.total_planned = sum(rec.mapped('task_ids.subtotal'))
