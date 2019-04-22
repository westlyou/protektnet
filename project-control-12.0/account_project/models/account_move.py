# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        copy=False,)
