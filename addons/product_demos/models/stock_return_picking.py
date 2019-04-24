# Copyright 2019 Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    is_cancel = fields.Boolean(
        string='Cancel the order',
    )

    def create_returns(self):
        res = super(StockReturnPicking, self).create_returns()
        if self.is_cancel:
            self.picking_id.sale_id.state = 'cancel'
        return res
