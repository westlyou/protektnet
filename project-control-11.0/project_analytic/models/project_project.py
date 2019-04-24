# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        help="Link this project to an analytic account if you need financial"
        " management on projects. It enables you to connect projects with"
        " budgets, planning, cost and revenue analysis, "
        "timesheets on projects, etc.",
        ondelete="cascade",
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        analytic_account = self.env['account.analytic.account'].create({
            'name': vals.get('name'),
            'project_id': res.id,
        })
        res.analytic_account_id = analytic_account.id
        return res

    @api.multi
    def write(self, vals):
        to_write = self
        for rec in self:
            if 'name' in vals:
                super(ProjectProject, rec).write(vals)
                rec.analytic_tag_id.name = rec.name
                to_write -= rec
        return super(ProjectProject, to_write).write(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.analytic_account_id:
                rec.analytic_account_id.unlink()
        return super().unlink()
