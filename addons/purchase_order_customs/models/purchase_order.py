# -*- coding: utf-8 -*-
# Copyright 2018, Grupo Censere (<https://www.grupocensere.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('partner_id', 'company_id')
    def _onchage_partner_id(self):
        if self.company_id.id == self.env.ref('__export__.res_company_4').id:
            self.partner_id = self.env.ref('__export__.res_partner_890').id


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            vendor = self.product_id.seller_ids.with_context(
                vendor=self.partner_id).filtered(
                    lambda r: r.name == r._context.get('vendor'))
            if not vendor:
                raise ValidationError(
                    _('This product "%s" does not have a price set for this '
                      'seller "%s". Please contact the administrator.') % (
                        self.product_id.name, self.order_id.partner_id.name))
            self.price_unit = vendor.price
