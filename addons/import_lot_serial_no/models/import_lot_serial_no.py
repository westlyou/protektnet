# -*- coding: utf-8 -*-
# Part of BrowseInfo.See LICENSE file for full copyright and licensing details.

import binascii
import tempfile
from tempfile import TemporaryFile

import xlrd
from odoo import _, api, fields, models
from odoo.exceptions import Warning

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class import_lot_wizard(models.TransientModel):

    _name = 'import.lot.wizard'

    select_lot = fields.Selection([
        ('serial', 'Serial No'),
        ('lot', 'Lot No')],
        string="Selection", default='serial')
    lot_file = fields.Binary(string="Select File")
    stock_move_id = fields.Many2one('stock.move')

    @api.multi
    def import_lots(self):
        if not self.lot_file:
            raise Warning(_("Please upload file first."))
        
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.lot_file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        res = False
        tot = 0.0
        move_active_id = self.env[self._context.get('active_model')].browse(
            self._context.get('active_id'))
        if self.select_lot == 'serial':
            if sheet.nrows-1 > move_active_id.product_uom_qty:
                raise Warning(
                    _("Your file contains more quantity then initial demand."))
        else:
            for row_no in range(sheet.nrows):
                if row_no <= 0:
                    fields = list(map(
                        lambda row: row.value.encode('utf-8'),
                        sheet.row(row_no)))
                else:
                    line = list(map(
                        lambda row: isinstance(row.value, bytes) and
                        row.value.encode('utf-8') or str(row.value),
                        sheet.row(row_no)))
                    tot += float(line[1])
            if tot > move_active_id.product_uom_qty:
                raise Warning(
                    _("Your file contains more quantity then initial demand."))
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                fields = list(map(
                    lambda row: row.value.encode('utf-8'),
                    sheet.row(row_no)))
            else:
                try:
                    line = list(map(
                        lambda row: isinstance(row.value, bytes) and
                        row.value.encode('utf-8') or str(row.value),
                        sheet.row(row_no)))
                    if self.select_lot == 'serial':
                        if len(line) == 1:
                            values.update({'lot': str(line[0])})
                        else:
                            raise Warning(
                                _("Format of excel file is inappropriate, "
                                    "Please provide File with proper format."))
                    else:
                        if len(line) == 2:
                            values.update({
                                'lot': str(line[0]),
                                'qty': line[1]
                            })
                        else:
                            raise Warning(_(
                                "Format of excel file is inappropriate, "
                                "Please provide File with proper format."))
                    res = self.create_lot_line(values)
                except IndexError:
                    raise Warning(_("You have selected wrong option"))
        # return res
        # return view of stock
        view = self.env.ref('stock.view_stock_move_operations')
        stock_pack_id = self.stock_move_id
        if stock_pack_id:
            ctx = dict(
                    stock_pack_id.env.context,
                    show_lots_m2o=(
                        stock_pack_id.has_tracking != 'none' and
                        (stock_pack_id.picking_type_id.use_existing_lots or
                            stock_pack_id.state == 'done' or
                            stock_pack_id.origin_returned_move_id.id)),
                    # able to create lots, whatever the value
                    # of ` use_create_lots`.
                    show_lots_text=(
                        stock_pack_id.has_tracking != 'none' and
                        stock_pack_id.picking_type_id.use_create_lots and not
                        stock_pack_id.picking_type_id.use_existing_lots and
                        stock_pack_id.state != 'done' and not
                        stock_pack_id.origin_returned_move_id.id),
                    show_source_location=stock_pack_id.location_id.child_ids,
                    show_destination_location=(
                        stock_pack_id.location_dest_id.child_ids),
                    show_package=(
                        not stock_pack_id.location_id.usage == 'supplier'),
                    show_reserved_quantity=stock_pack_id.state != 'done',
                )

            ctx.update({'raise-exception': False})

            return {
                'name': _('Detailed Operations'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.move',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': stock_pack_id.id,
                'context': ctx
            }
        else:
            return res

    @api.multi
    def create_lot_line(self, values):
        list_lot = []
        lot = values.get('lot')
        stock_pack_id = self.env['stock.move'].browse(
            self._context.get('active_id'))
        if (self.select_lot == 'lot' or
                stock_pack_id.product_id.tracking == 'lot'):
            if stock_pack_id.picking_type_id.code == 'incoming':
                lot_id = self.find_lot(values.get('lot'))
                move_assing = self.env['stock.move.line'].search([
                    ('move_id', '=', self.stock_move_id.id),
                    ('lot_id', '=', False)], limit=1)
                move_assing.write({
                    'lot_id': lot_id.id,
                    'lot_name': lot_id.name,
                    'product_uom_id': lot_id.product_id.uom_id.id,
                    'qty_done': 1,
                })
            else:
                lot_id = self.env['stock.production.lot'].search([
                    ('name', '=', values.get('lot'))])
                if lot_id and lot_id[0]:
                    lot_id = lot_id[0]
                    move_assing = self.env['stock.move.line'].search([
                        ('move_id', '=', self.stock_move_id.id),
                        ('lot_id', '=', False)], limit=1)
                    move_assing.write({
                        'lot_id': lot_id.id,
                        'lot_name': lot_id.name,
                        'product_uom_id': lot_id.product_id.uom_id.id,
                        'qty_done': 1,
                    })
        else:
            if lot in list_lot:
                raise Warning(_(
                    'You have already mentioned this lot name in '
                    'another line'))
            else:
                if stock_pack_id.picking_code == 'incoming':
                    lot_id = self.find_lot(values.get('lot'))
                    move_assing = self.env['stock.move.line'].search([
                        ('move_id', '=', self.stock_move_id.id),
                        ('lot_id', '=', False)], limit=1)
                    move_assing.write({
                        'lot_id': lot_id.id,
                        'lot_name': lot_id.name,
                        'product_uom_id': lot_id.product_id.uom_id.id,
                        'qty_done': 1,
                    })
                else:
                    lot_id = self.env['stock.production.lot'].search([
                        ('name', '=', values.get('lot'))])
                    if lot_id and lot_id[0]:
                            lot_id = lot_id[0]
                            move_assing = self.env['stock.move.line'].search([
                                ('move_id', '=', self.stock_move_id.id),
                                ('lot_id', '=', False)], limit=1)
                            move_assing.write({
                                'lot_id': lot_id.id,
                                'lot_name': lot_id.name,
                                'product_uom_id': lot_id.product_id.uom_id.id,
                                'qty_done': 1,
                            })
                    else:
                        raise Warning("Lot number Not Available")

        list_lot.append(lot)

    @api.multi
    def find_lot(self, lot):
        stock_pack_id = self.env['stock.move'].browse(
            self._context.get('active_id'))
        production_lot_id = self.env['stock.production.lot'].create({
            'name': lot,
            'product_id': stock_pack_id.product_id.id,
            'product_uom_id': stock_pack_id.product_id.uom_id.id,
        })
        return production_lot_id


class stock_move(models.Model):

    _inherit = 'stock.move'

    @api.multi
    def open_serial_wizard(self):
        view = self.env.ref('import_lot_serial_no.lot_wizard_view')
        ctx = {}
        ctx.update({'default_stock_move_id': self.id})
        return {
            'name': _('Import Lots'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.lot.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': ctx
        }
