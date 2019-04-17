# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.constrains('quantity')
    def check_quantity(self):
        for quant in self:
            if (float_compare(quant.quantity, 1,
                              precision_rounding=quant.product_uom_id.rounding
                              ) > 0 and quant.lot_id and
                    quant.product_id.tracking == 'serial' and
                    quant.lot_id.company_id == self.env.user.company_id):
                raise ValidationError(
                    _('A serial number should only be linked '
                        'to a single product.'))
