# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_count = fields.Integer(
        string='Purchases',
        compute='_compute_purchase_count'
    )

    @api.depends('order_line')
    def _compute_purchase_count(self):
        for rec in self:
            pos = self.env['purchase.order.line'].search([
                ('sale_line_id', 'in',
                    rec.mapped('order_line').ids)]).mapped('order_id')
            rec.purchase_count = len(pos)

    @api.multi
    def action_view_purchase(self):
        context = dict(self._context or {})
        pos = self.env['purchase.order.line'].search([
            ('sale_line_id', 'in',
                self.mapped('order_line').ids)]).mapped('order_id')
        return {
            'name': _('Purchase Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', pos.ids)],
            'context': context,
        }


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    serial_numbers = fields.Char(
        string='Serial Numbers',
    )
