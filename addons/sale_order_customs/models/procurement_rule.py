# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    @api.multi
    def _prepare_purchase_order_line(
            self, product_id, product_qty, product_uom, values, po, supplier):

        res = super(ProcurementRule, self)._prepare_purchase_order_line(
            product_id, product_qty, product_uom, values, po, supplier)
        line = values.get('move_dest_ids').sale_line_id
        seller = product_id.seller_ids.with_context(
            vendor=po.partner_id).filtered(
            lambda x: x.name == x._context.get('vendor') and
            x.company_id == x.env.user.company_id)[0]
        if not seller:
            raise ValidationError(_('Warning! Seller bad configured.'))
        tax_id = res['taxes_id'][0][2]
        taxes_id = self.env['account.tax'].browse(tax_id)
        price_unit = self.env['account.tax']._fix_tax_included_price_company(
            seller.price, product_id.supplier_taxes_id, taxes_id,
            values['company_id']) if seller else 0.0
        if (price_unit and seller and po.currency_id and
                seller.currency_id != po.currency_id):
            price_unit = seller.currency_id.compute(price_unit, po.currency_id)
        if line:
            self.env['purchase.order'].browse(
                res['order_id']).name += " - " + line.order_id.name
            res.update({
                'sale_line_id': line.id,
                'x_studio_field_WAHdj': line.serial_numbers,
                'price_unit': price_unit,
            })
        return res

    def _prepare_purchase_order(
            self, product_id, product_qty, product_uom,
            origin, values, partner):
        res = super(ProcurementRule, self)._prepare_purchase_order(
            product_id, product_qty, product_uom, origin, values, partner)
        sale = values.get('group_id').sale_id
        res.update({
            'x_studio_field_jaeoa': sale.partner_id.id,
            'partner_id': self._get_partner_id(sale),
            'sale_order_id': sale.id,
            'x_start_date': sale.x_studio_field_nJisW,
            'x_end_date': sale. x_studio_field_vqN4P,
            'x_serial': sale.x_studio_field_wJcd2,
            'x_studio_field_xOOmu': sale.x_studio_field_JQBmy.id,
            'x_ingeniero_encargado': sale.x_studio_field_DRLTc,
            'x_additional_discount': sale.x_additional_discount,
            'x_studio_field_Oxp7D': sale.quote,
            'x_studio_field_4u1C2': sale.deal,
            'domain': sale.x_studio_field_PXOli,
            'memo': sale.x_studio_field_RmPpJ,
            'guide_number': sale.guide_number,
        })
        return res

    def _get_partner_id(self, sale):
        partner = sale.order_line.mapped(
            'product_id').mapped('variant_seller_ids').filtered(
            lambda x: x.company_id == x.env.user.company_id).mapped(
            'name').filtered(lambda x: x.id not in [722, 2428])
        if len(partner) > 1:
            return partner[0].id
        return partner.id
