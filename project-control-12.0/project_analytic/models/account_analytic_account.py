# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    _description = 'Analytic Account'

    project_id = fields.Many2one(
        'project.project',
        string='Project',)

    @api.multi
    def unlink(self):
        projects = self.env['project.project'].search(
            [('analytic_account_id', 'in', self.ids)])
        has_tasks = self.env['project.task'].search_count(
            [('project_id', 'in', projects.ids)])
        if has_tasks:
            raise ValidationError(
                _('Please remove existing tasks in the project'
                    ' linked to the accounts you want to delete.'))
        return super().unlink()

    @api.multi
    def projects_action(self):
        if self.project_id:
            result = {
                "type": "ir.actions.act_window",
                "res_model": "project.project",
                "views": [(False, "form")],
                "res_id": self.project_id.id,
                "context": {"create": False},
                "name": _("Project"),
            }
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result
