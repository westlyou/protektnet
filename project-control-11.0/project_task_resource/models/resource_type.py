# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResourceType(models.Model):
    _name = 'resource.type'
    _description = 'Resource Type'

    name = fields.Char()
