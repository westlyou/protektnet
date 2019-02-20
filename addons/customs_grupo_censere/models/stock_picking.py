# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('shipment', 'Shipment')])
