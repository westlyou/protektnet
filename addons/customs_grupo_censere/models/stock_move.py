# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    standard_price = fields.Float(
        string="Cost",
        related="move_id.purchase_line_id.price_unit")
    lst_price = fields.Float(
        string="List Price",
        related="product_id.lst_price")
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        related='move_id.picking_id.partner_id'
    )
    product_brand = fields.Selection(
        related='product_id.product_tmpl_id.product_brand',
        store=True, string="Brand")

    @api.model
    def create(self, vals):
        moves = super(StockMoveLine, self).create(vals)
        for res in moves:
            if (res.lot_id and res.product_uom_qty == 0.0 and
                    res.picking_id.picking_type_code == 'outgoing'):
                quant = res.lot_id.quant_ids.filtered(
                    lambda x: x.location_id.usage == 'internal' and
                    x.lot_id.company_id == x.env.user.company_id
                )
                if not quant:
                    picki = self.search([
                        ('location_id.usage', '=', 'internal'),
                        ('location_dest_id.usage', '=', 'customer'),
                        ('lot_id', '=', res.lot_id.id), ('state', '=', 'done')]
                    )
                    raise ValidationError(_(
                        "The serial number that was selected has already been "
                        "output, in the picking: %s, please check it.") %
                        picki.reference)
                sml_pickings = self.env['stock.move.line'].search([
                    ('lot_id', '=', res.lot_id.id),
                    ('state', '!=', 'done'),
                    ('product_uom_qty', '=', 1.0),
                    ('picking_id', '!=', res.picking_id.id)])
                if sml_pickings:
                    for sml_picking in sml_pickings:
                        sml_picking.state = 'waiting'
                        sml_picking.lot_id = False
                        sml_picking.product_uom_qty = '0'
                        sml_picking.unlink()
                    if quant.reserved_quantity == 1.0:
                        quant.sudo().reserved_quantity = 0.0
                    res.product_uom_qty = 1.0
                if not sml_pickings:
                    if quant.reserved_quantity == 1.0:
                        quant.reserved_quantity = 0.0
                    res.sudo().product_uom_qty = 1.0
                quant.reserved_quantity = 1.0
        return moves
