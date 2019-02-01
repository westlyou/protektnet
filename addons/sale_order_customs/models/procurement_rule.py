# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    @api.multi
    def _prepare_purchase_order_line(
            self, product_id, product_qty, product_uom, values, po, supplier):
        res = super(ProcurementRule, self)._prepare_purchase_order_line(
            product_id, product_qty, product_uom, values, po, supplier)
        line = values.get('move_dest_ids').sale_line_id
        res['sale_line_id'] = line.id
        res['x_studio_field_WAHdj'] = line.serial_numbers
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
