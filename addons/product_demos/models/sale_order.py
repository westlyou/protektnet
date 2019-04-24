# Copyright 2019 Grupo Censere (http://grupocensere.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_demo = fields.Boolean(
        compute="_compute_invoice_demo",
        string="Is Demo"
    )

    @api.depends('order_line')
    def _compute_invoice_demo(self):
        for rec in self:
            rec.is_demo = bool(
                rec.order_line.mapped('route_id').filtered(
                    lambda route: route.push_ids))
