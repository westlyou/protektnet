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

    @api.one
    def _prepare_sale_order_data(
            self, name, partner, company, direct_delivery_address):
        res = super(PurchaseOrder, self)._prepare_sale_order_data(
            name, partner, company, direct_delivery_address)
        res[0].update({
            'x_studio_field_nJisW': self.x_start_date,
            'x_studio_field_vqN4P': self.x_end_date,
            'x_studio_field_wJcd2': self.x_serial,
            'x_studio_field_JQBmy': self.x_studio_field_xOOmu.id,
            'x_studio_field_DRLTc': self.x_ingeniero_encargado.id,
            'x_additional_discount': self.x_additional_discount,
            'x_studio_field_GC23d': self.sale_order_id.x_studio_field_GC23d,
            'x_studio_field_iu2yo': self.sale_order_id.x_studio_field_iu2yo,
        })
        return res[0]

    @api.model
    def _prepare_sale_order_line_data(self, line, company, sale_id):
        res = super(PurchaseOrder, self)._prepare_sale_order_line_data(
            line, company, sale_id)
        res.update({
            'serial_numbers': line.x_studio_field_WAHdj
        })
        return res


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
