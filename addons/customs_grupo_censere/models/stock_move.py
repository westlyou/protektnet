# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'stock.move.line'

    standard_price = fields.Float(
        string="Cost",
        related="move_id.purchase_line_id.price_unit")
    lst_price = fields.Float(
        string="List Price",
        related="product_id.list_price")
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        related='move_id.picking_id.partner_id'
    )
    product_brand = fields.Selection(
        related='product_id.product_tmpl_id.product_brand',
        store=True, string="Brand")
