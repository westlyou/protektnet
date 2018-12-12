# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    _sql_constraints = [
        ('name_ref_uniq', 'Check(1=1)',
         'The combination of serial number and product must be unique !'),
    ]
