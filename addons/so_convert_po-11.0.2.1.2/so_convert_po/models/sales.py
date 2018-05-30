# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


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
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'sale_order_id': self.id,
            'x_start_date': self.x_studio_field_nJisW,
            'x_end_date': self.	x_studio_field_vqN4P,
            'x_serial': self.x_studio_field_wJcd2,

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
                'x_serial': line.x_studio_field_6P3b4,
            })
