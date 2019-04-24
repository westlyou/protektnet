# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_template = fields.Boolean(
        string='Is a template?',
        copy=False,
    )
