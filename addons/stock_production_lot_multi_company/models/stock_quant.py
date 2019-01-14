# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.quant'

    @api.constrains('quantity')
    def check_quantity(self):
        for quant in self:
            if (float_compare(
                    quant.quantity, 1,
                    precision_rounding=quant.product_uom_id.rounding) > 0 and
                    quant.lot_id and quant.product_id.tracking == 'serial' and
                    quant.company_id == quant.lot_id.company_id):
                raise ValidationError(
                    _('A serial number should only be linked '
                        'to a single product.'))
