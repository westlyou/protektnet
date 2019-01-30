# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import calendar
import io
from datetime import datetime

from odoo import _, api, fields, models

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReportSaleWizard(models.TransientModel):
    _name = "report.sale.wizard"

    file_xlsx = fields.Binary(
        string='File',
    )
    file_xlsx_name = fields.Char(
        string='File Name',
    )
    state = fields.Selection(
        [('choose', 'choose'), ('get', 'get')], default='choose')
    start_date = fields.Date(
        string="From Date", required='1',
        default=lambda self: self.get_date_start(),)
    end_date = fields.Date(
        string="To Date", required='1',
        default=lambda self: self.get_date_end(),)
    licenses = fields.Boolean(
        string='Linceses',
    )
    serials = fields.Boolean(
        string='Serials',
    )
    product_brand = fields.Selection([
        ('all', 'All'),
        ('Airtight', 'Airtight'), ('Barracuda', 'Barracuda'),
        ('Bitdefender', 'Bitdefender'), ('Bugooro', 'Bugooro'),
        ('Cautio', 'Cautio'), ('Consulting', 'Consulting'),
        ('Cyberoam', 'Cyberoam'), ('EndPoint', 'EndPoint'),
        ('Expand', 'Expand'), ('FatPipe', 'FatPipe'),
        ('GrandStream', 'GrandStream'), ('HanDreamNet', 'HanDreamNet'),
        ('Hauri', 'Hauri'), ('Infoblox', 'Infoblox'),
        ('InterGuard', 'InterGuard'), ('IP Guard', 'IP Guard'),
        ('IP Scan', 'IP Scan'), ('Juniper', 'Juniper'),
        ('LogRhythm', 'LogRhythm'), ('Lok-it', 'Lok-it'),
        ('LUMEN CACHE', 'LUMEN CACHE'), ('M86', 'M86'),
        ('Mykonos', 'Mykonos'), ('NCP', 'NCP'), ('nProtect', 'nProtect'),
        ('Okiok', 'Okiok'), ('otros', 'otros'), ('Portafolio', 'Portafolio'),
        ('Rackmount', 'Rackmount'), ('Remote Call', 'Remote Call'),
        ('Servicios', 'Servicios'), ('Somansa', 'Somansa'),
        ('Sophos', 'Sophos'), ('Spamina', 'Spamina'),
        ('Spector', 'Spector'), ('Terranova', 'Terranova')],
        string="Brands", default="all")

    @api.model
    def get_date_start(self):
        today = datetime.now()
        month = today.month
        date_string = "%s-%s-01"
        if month < 10:
            date_string = "%s-0%s-01"
        month_start = date_string % (today.year, month)
        return month_start

    @api.model
    def get_date_end(self):
        today = datetime.now()
        month = today.month
        date_string = "%s-%s-%s"
        if month < 10:
            date_string = "%s-0%s-%s"
        month_end = date_string % (
            today.year, today.month, calendar.monthrange(
                today.year - 1, month)[1])
        return month_end

    def create_data(self):
        sol = self.env['sale.order.line']
        domain = [
            ('order_id.date_order', '>=', self.start_date),
            ('order_id.date_order', '<=', self.end_date),
            ('company_id', '=', self.env.user.company_id.id),
            ('state', '=', 'sale'),
        ]
        if self.product_brand != 'all':
            domain.append(
                ('product_id.product_tmpl_id.x_studio_field_U36cw', '=',
                    self.product_brand))
        if self.licenses and self.serials:
            domain.append(
                ('product_id.categ_id', 'in', [4, 5]))
        if self.licenses and not self.serials:
            domain.append(
                ('product_id.categ_id', 'in', [5]))
        if not self.licenses and self.serials:
            domain.append(
                ('product_id.categ_id', 'in', [4]))
        so_lines = sol.search(domain)
        so_lines_group = sol.read_group(
            [('product_id', 'in', so_lines.mapped('product_id').ids)],
            ['product_id', 'product_uom_qty',
             'price_subtotal', 'product_id.x_studio_field_U36cw'],
            ['product_id'])
        sorted_product_records = []
        for so_line in so_lines_group:
            sorted_product_records.append({
                'name': so_line.get('product_id')[1],
                'qty': so_line.get('product_uom_qty'),

                'total': so_line.get('price_subtotal'),
            })
        return sorted_product_records

    def print_xls_report(self):
        data = self.create_data()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('stock_rackmount')

        title_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2})
        style = workbook.add_format({
            'font_name': 'Arial',
            'bold': False,
            'top': 2,
            'left': 2,
            'right': 2,
            'bottom': 2,
        })

        sheet.set_column(0, 0, 15)
        sheet.write(0, 0, '', title_style)

        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })

        binary_data = self.env.user.company_id.logo
        image = io.BytesIO(base64.b64decode(binary_data))
        sheet.set_row(0, 100)
        sheet.merge_range('A1:C1', ' ', merge_format)
        sheet.insert_image(
            'A1:D1', 'image',
            {'image_data': image, 'x_offset': 15, 'y_offset': 10})
        sheet.merge_range('A2:D2', self.env.user.company_id.name, merge_format)
        sheet.merge_range('A3:B3', _('Sales'), merge_format)
        sheet.write('C3', fields.Date.context_today(self), merge_format)
        x = 0
        y_offset = 3
        for column in ['Product', 'Quantity', 'Total']:
            sheet.write(
                y_offset, x,
                column, title_style)
            x += 1
        y_offset += 1

        sheet.set_column('A:A', max([len(line['name']) for line in data]))
        sheet.set_column('B:B', len('Quantity'))
        sheet.set_column('C:C', max(
            [len(str(line['total'])) for line in data]))
        for row in range(0, len(data)):
            sheet.write(row + y_offset, 0, data[row]['name'], style)
            sheet.write(row + y_offset, 1, data[row]['qty'], style)
            sheet.write(row + y_offset, 2, data[row]['total'], style)

        workbook.close()
        output.seek(0)
        self.file_xlsx = base64.encodebytes(output.read())
        self.file_xlsx_name = 'report_sales.xlsx'
        self.write({'state': 'get'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'report.sale.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
