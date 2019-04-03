# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allow_convert = fields.Boolean(
        "Allow convert SO to Purchase Order",
        compute='_compute_allow_convert',
    )

    @api.one
    @api.depends('state')
    def _compute_allow_convert(self):
        # Generate field name to search value from settings,
        # if there's no field with generated name, will return False.
        self.allow_convert = self.env['res.config.settings'].get_values().get(
            'so_' + self.state + '_allow_convert_po')

    @api.multi
    def action_show_related_purchase_order(self):
        self.ensure_one()
        return {
            'name': _("Related Purchase Order"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'view_id': False,
            'res_id': self.purchase_order_id.id,
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def action_convert_to_purchase_order(self):
        self.ensure_one()
        default_so_state = (
            self.env['res.config.settings'].get_values().get('so_state'))
        self.purchase_order_id = self.env['purchase.order'].create({
            'state': default_so_state,
            'x_studio_field_jaeoa': self.partner_id.id,
            'partner_id': self.get_partner_id(),
            'currency_id': self.get_partner_id(
            ).property_purchase_currency_id.id,
            'sale_order_id': self.id,
            'x_start_date': self.x_studio_field_nJisW,
            'x_end_date': self.	x_studio_field_vqN4P,
            'x_serial': self.x_studio_field_wJcd2,
            'x_studio_field_xOOmu': self.x_studio_field_JQBmy.id,
            'x_ingeniero_encargado': self.x_studio_field_DRLTc,
            'x_additional_discount': self.x_additional_discount,
            'x_studio_field_Oxp7D': self.quote,
            'x_studio_field_4u1C2': self.deal,
            'domain': self.x_studio_field_PXOli,
            'memo': self.x_studio_field_RmPpJ,
            'guide_number': self.guide_number,

        })
        self.purchase_order_id.name += " - " + self.name
        for line in self.order_line:
            self.env['purchase.order.line'].create({
                'order_id': self.purchase_order_id.id,
                'name': line.name,
                'date_planned': fields.Datetime.now(),
                'product_id': line.product_id.id,
                'product_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                'x_studio_field_WAHdj': line.serial_numbers,
            })

    def get_partner_id(self):
        partner = self.order_line.mapped(
            'product_id').mapped('seller_ids').filtered(
            lambda x: x.company_id == x.env.user.company_id
        ).mapped('name').filtered(
            lambda x: x.id not in [722, 2428])
        if not partner:
            raise ValidationError('Error in configuration of the sellers')
        if len(partner) > 1:
            return partner[0].id
        return partner.id
