# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    analytic_tag_id = fields.Many2one(
        'account.analytic.tag',
        string='Analytic Tag',
    )

    @api.model
    def create(self, vals):
        analytic_tag = self.env['account.analytic.tag'].create({
            'name': vals.get('name'),
        })
        vals['analytic_tag_id'] = analytic_tag.id
        return super().create(vals)

    @api.multi
    def write(self, vals):
        to_write = self
        for rec in self:
            if 'name' in vals:
                super(ProjectTask, rec).write(vals)
                rec.analytic_tag_id.name = rec.name
                to_write -= rec
        return super(ProjectTask, to_write).write(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.analytic_tag_id:
                rec.analytic_tag_id.unlink()
        return super().unlink()
