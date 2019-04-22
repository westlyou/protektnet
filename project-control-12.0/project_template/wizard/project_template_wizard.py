# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.translate import _


class ProjectTemplateWizard(models.TransientModel):
    _name = 'project.template.wizard'

    name = fields.Char(required=True,)
    project_id = fields.Many2one(
        comodel_name='project.project',
        string="Project",
        domain=[('is_template', '=', True)],
        required=True,
    )

    @api.multi
    def create_from_template(self):
        self.ensure_one()
        template = self.project_id.copy(
            {'name': self.name})
        body = self.env['ir.qweb'].render(
            'project_template.project_template_message',
            {'self': self.project_id})
        template.message_post(body=body)
        return {
            'name': _('Project Template'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': template.id,
            'type': 'ir.actions.act_window',
            'context': {
                'create': False,
                'delete': False,
            }
        }
