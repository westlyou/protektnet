# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    wbs_element_id = fields.Many2one(
        comodel_name='project.wbs_element',
        string='WBS Element',
    )

    @api.onchange('wbs_element_id')
    def _onchange_wbs_element_id(self):
        if self.wbs_element_id:
            self.project_id = self.wbs_element_id.project_id

    @api.multi
    @api.constrains('wbs_element_id')
    def _check_wbs_element_assigned(self):
        for record in self:
            if record.wbs_element_id and record.wbs_element_id.child_ids:
                raise ValidationError(
                    _('A WBS Element that is parent'
                        ' of others cannot have'
                        ' tasks assigned.'))
