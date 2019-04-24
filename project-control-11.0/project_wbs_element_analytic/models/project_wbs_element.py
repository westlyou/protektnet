# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    analytic_tag_id = fields.Many2one(
        'account.analytic.tag',
        string='Analytic Tag',
    )

    @api.model
    def create(self, values):
        rec = super().create(values)
        name = '[%s] / %s - %s' % (rec.project_id.name, rec.code, rec.name)
        rec.analytic_tag_id = rec.analytic_tag_id.create({'name': name, })
        return rec

    @api.multi
    def write(self, values):
        to_write = self
        for rec in self:
            if 'name' in values or 'code' in values:
                super(ProjectWbsElement, rec).write(values)
                name = '[%s] / %s - %s' % (
                    rec.project_id.name, rec.code, rec.name)
                rec.analytic_tag_id.name = name
                to_write -= rec
        return super(ProjectWbsElement, to_write).write(values)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.analytic_tag_id:
                rec.analytic_tag_id.unlink()
        return super().unlink()
