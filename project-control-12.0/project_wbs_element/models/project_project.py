# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    wbs_element_ids = fields.One2many(
        comodel_name='project.wbs_element',
        inverse_name='project_id',
    )
    nbr_wbs_elements = fields.Integer(
        'Number of WBS Elements',
        compute='_compute_count_wbs_elements',)

    @api.depends('wbs_element_ids')
    def _compute_count_wbs_elements(self):
        for record in self:
            record.nbr_wbs_elements = len(record.wbs_element_ids)
