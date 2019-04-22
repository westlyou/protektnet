# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def create(self, vals):
        ml = super(StockMoveLine, self).create(vals)
        if (ml.move_id.purchase_line_id.order_id.sale_order_id.
                client_order_ref and self.env.user.company_id.id == 3):
            self.env['stock.production.lot'].create({
                'name': ml.lot_id.name,
                'product_id': ml.product_id.id,
                'company_id': 1,
            })
        return ml
