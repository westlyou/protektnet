
# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import ast
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delevery_status = fields.Selection(
        [('done', 'Done'),
         ('waiting', 'Waiting'),
         ('pending', 'Pending'), ],
        string='Delevery Status',
        compute='_compute_delevery_status',
        store=True, readonly=True)
    guide_number = fields.Char(
        string='Tracking Number',
    )

    @api.depends('order_line')
    def _compute_delevery_status(self):
        for sale in self:
            qty_delevery = sum(self.order_line.filtered(
                lambda x: x.product_id.type != 'service'
            ).mapped('qty_delivered'))
            product_uom_qty = sum(self.order_line.filtered(
                lambda x: x.product_id.type != 'service'
            ).mapped('product_uom_qty'))
            if qty_delevery == 0.0:
                sale.delevery_status = 'pending'
            if product_uom_qty == qty_delevery:
                sale.delevery_status = 'done'
            if product_uom_qty > qty_delevery and qty_delevery != 0.0:
                sale.delevery_status = 'waiting'


    @api.multi
    def action_view_delivery(self):
        action = super(SaleOrder, self).action_view_delivery()
        return self.restrition_validation(action)

    @api.multi
    def action_view_invoice(self):
        action = super(SaleOrder, self).action_view_invoice()
        return self.restrition_validation(action)

    def restrition_validation(self, action):
        if (not self.env.user.has_group('sales_team.group_sale_manager') and
                self.env.user.has_group(
                    'sales_team.group_sale_salesman_all_leads')):
            test = action['context'].replace(' ', '').replace('\n', '')
            dict_test = ast.literal_eval(test)
            dict_test.update({'create': False, 'edit': False})
            action['context'] = dict_test
        return action
