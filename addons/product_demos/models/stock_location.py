# Copyright 2019 Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    demo_location = fields.Boolean(
        string='¿Es una ubicación de demos?',
    )
