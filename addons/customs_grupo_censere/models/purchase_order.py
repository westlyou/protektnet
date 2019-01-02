# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import ast
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "purchase.order"

    delevery_status = fields.Selection(
        [('done', 'Done'),
         ('waiting', 'Waiting'),
         ('confirmed', 'Confirmed'), ],
        string='Delevery Status',
        compute='_compute_delevery_status',
        store=True, readonly=True)

    @api.depends('picking_ids')
    def _compute_delevery_status(self):
        for purchase in self:
            if purchase.picking_ids:
                if all([picking.state in ['done', 'cancel']
                        for picking in purchase.picking_ids]):
                    purchase.delevery_status = 'done'
                if (any([picking.state == 'done'
                         for picking in purchase.picking_ids])and
                        any([picking.state not in ['done', 'cancel']
                             for picking in purchase.picking_ids])):
                    purchase.delevery_status = 'waiting'
                if all([picking.state != 'done'
                        for picking in purchase.picking_ids]):
                    purchase.delevery_status = 'confirmed'
