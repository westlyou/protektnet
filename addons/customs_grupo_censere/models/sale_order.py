# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import ast
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delevery_status = fields.Selection(
        [('done', 'Done'),
         ('waiting', 'waiting'),
         ('confirmed', 'Confirmed'), ],
        string='Delevery Status',
        compute='_compute_delevery_status',
        store=True, readonly=True)
    guide_number = fields.Char(
        string='Guide Number',
    )

    @api.depends('picking_ids')
    def _compute_delevery_status(self):
        for sale in self:
            if sale.picking_ids:
                if all([picking.state in ['done', 'cancel']
                        for picking in sale.picking_ids]):
                    sale.delevery_status = 'done'
                if (any([picking.state == 'done'
                         for picking in sale.picking_ids])and
                        any([picking.state not in ['done', 'cancel']
                             for picking in sale.picking_ids])):
                    sale.delevery_status = 'waiting'
                if all([picking.state != 'done'
                        for picking in sale.picking_ids]):
                    sale.delevery_status = 'confirmed'

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
