# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64

import io
from odoo import _, api, fields, models
import calendar
from odoo.exceptions import ValidationError
from datetime import datetime
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ResCompany(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def get_date_start(self):
        today = datetime.now()
        # month = today.month
        month = 1
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

    def send_mail_rackmount(self, name, email_to, email_from, id_server):
        mail = self.env['mail.mail']
        values = self._prepare_values(name, email_to, email_from, id_server)
        mail.with_context(cron_server=True).create(values)
        mail.send()
        self.env['ir.attachment'].search([(
            'name', '=',
            'Stock Kardex_' + fields.Date.context_today(self),)])

    def _prepare_values(self, name, email_to, email_from, server):
        url = 'data:image/png;base64,%s'
        return {
            'subject': name + "/" + fields.Date.context_today(self),
            'author_id': self.env.user.partner_id.id,
            'email_from': email_from,
            'email_to': email_to,
            'attachment_ids': [(6, 0, [self.create_attachment()])],
            'mail_server_id': server,
            'body_html': (
                '<table width="650" border="0" cellpadding="0" '
                'bgcolor="#875A7B" style="text-align: left; '
                'background-color: rgb(135, 90, 123); min-width: 590px; '
                'padding: 20px;">'
                '<tbody><tr>'
                '<td valign="middle" style="text-align: left;">'
                '<span style="font-size: 20px; color: white; '
                'font-weight: bold;">Stock of Rackmount</span></td>'
                '<td valign="middle" align="right" style="text-align: left;">'
                '<img t-if="company.logo" t-att-src="' + url +
                ' % to_text(company.logo)" class="pull-left"/>'
                '</td></tr></tbody></table><table width="650" border="0" '
                'cellpadding="0" bgcolor="#ffffff" style="text-align: left; '
                'background-color: rgb(255, 255, 255); min-width: 590px; '
                'padding: 20px;"><tbody><tr><td valign="top" style="color: '
                'rgb(85, 85, 85); font-size: 14px;">Adjunto el inventario '
                'que se tiene de la marca hasta el dia.</td></tr></tbody>'
                '</table><table width="650" border="0" cellpadding="0" '
                'bgcolor="#875A7B" style="text-align: left; background-color: '
                'rgb(135, 90, 123); min-width: 590px; padding: 20px;"><tbody>'
                '<tr><td valign="middle" style="padding-top: 10px; '
                'padding-bottom: 10px; color: rgb(255, 255, 255); '
                'font-size: 12px; text-align: left;">' +
                self.env.user.company_id.name + '<br>' +
                self.env.user.company_id.phone + '</td><td valign="middle" '
                'align="right" style="padding-top: 10px; padding-bottom: '
                '10px; color: rgb(255, 255, 255); font-size: 12px;">'
                '<a href="mailto:$%7B' + self.env.user.company_id.email +
                '%7D" style="color: white;">' +
                self.env.user.company_id.email + '</a><br>'
                '<a href="' + self.env.user.company_id.website +
                '"style="color: white;">' +
                self.env.user.company_id.website + '</a></td>'
                '</tr></tbody></table><p style="text-align: left;">'
                'Powered by&nbsp;<a href="https://www.odoo.com/">Odoo</a>.'
                '<br></p>')
        }

    def get_columns_name(self):
        return [
            {'name': '' if not self._context.get('print_mode', False)
                else _("Product")},
            {'name': _("Type")if not self._context.get('print_mode', False)
                else ""},
            {'name': (
                _("Date") if not self._context.get('print_mode', False)
                else ""), 'class': 'date'},
            {'name': (
                _("Quantity") if not self._context.get('print_mode', False)
                else ""), 'class': 'number'},
            {'name': _("UoM")},
            {'name': "" if not self._context.get('print_mode', False)
                else _("Description")},
            {'name': _("Stock"), 'class': 'number'},
            {'name': _("MSRP"), 'class': 'number'},
        ]

    def create_attachment(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('stock_rackmount')
        title_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2})
        level_2_style = workbook.add_format({
            'font_name': 'Arial',
            'bold': False,
            'top': 2})
        level_2_style.set_text_wrap()
        level_2_style_left = workbook.add_format({
            'font_name': 'Arial',
            'bold': False,
            'top': 2,
            'left': 2})
        level_2_style_right = workbook.add_format({
            'font_name': 'Arial',
            'bold': False,
            'top': 2,
            'right': 2})
        upper_line_style = workbook.add_format({
            'font_name': 'Arial', 'top': 2})

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
        sheet.merge_range('A1:E1', ' ', merge_format)
        sheet.insert_image(
            'A1:E1', 'image',
            {'image_data': image, 'x_offset': 15, 'y_offset': 10})
        sheet.merge_range('A2:E2', self.env.user.company_id.name, merge_format)
        sheet.merge_range('A2:E2', self.env.user.company_id.name, merge_format)
        sheet.merge_range('A3:B3', _('Stock Kardex'), merge_format)
        sheet.merge_range(
            'C3:E3', fields.Date.context_today(self), merge_format)
        x = 0
        y_offset = 3
        for column in [x for x in self.with_context(
                print_mode=True).get_columns_name() if len(x['name']) > 1]:
            sheet.write(
                y_offset, x,
                column.get('name', '').replace(
                    '<br/>', ' ').replace('&nbsp;', ' '), title_style)
            x += 1
        y_offset += 1
        lines = self.get_lines()
        if lines:
            max_width = max([len(l['columns']) for l in lines])
        sheet.set_column('A:A', max([len(x['name']) for x in lines]))
        sheet.set_column(
            'B:B', max([len(x['columns'][0]['name']) for x in lines]))
        sheet.set_column(
            'C:C', 50)
        sheet.set_column(
            'D:D', max([len(x['columns'][2]['name']) for x in lines]))
        sheet.set_column(
            'E:E', max([len(x['columns'][3]['name']) for x in lines]))
        for y in range(0, len(lines)):
            if lines[y].get('level') == 2:
                style_left = level_2_style_left
                style_right = level_2_style_right
                style = level_2_style
            sheet.write(y + y_offset, 0, lines[y]['name'], style_left)
            for x in range(1, max_width - len(lines[y]['columns']) + 1):
                sheet.write(y + y_offset, x, None, style)
            for x in range(1, len(lines[y]['columns']) + 1):
                if x < len(lines[y]['columns']):
                    sheet.write(
                        y + y_offset,
                        x, lines[y][
                            'columns'][x - 1].get('name', ''), style)
                else:
                    sheet.write(
                        y + y_offset,
                        x, lines[y][
                            'columns'][x - 1].get('name', ''), style_right)
            if 'total' in lines[y].get(
                    'class', '') or lines[y].get('level') == 0:
                for x in range(len(lines[0]['columns']) + 1):
                    sheet.write(y + 1 + y_offset, x, None, upper_line_style)
                y_offset += 1
        if lines:
            for x in range(max_width + 1):
                sheet.write(len(lines) + y_offset, x, None, upper_line_style)

        workbook.close()
        output.seek(0)
        attach_id = self.env['ir.attachment'].create({
            'name': 'Stock Kardex_' + fields.Date.context_today(self),
            'type': 'binary',
            'datas_fname': (
                'Stock_Kardex_' + fields.Date.context_today(self) +
                '.xlsx'),
            'datas': base64.encodebytes(output.read()),
        })
        return attach_id.id

    @api.model
    def get_initial_balance(self, product_id, date_from, location_id):
        total_out = 0.0
        total_in = 0.0
        moves_out = self.env['stock.move'].read_group(
            [('product_id', '=', product_id),
             ('location_id', '=', location_id),
             ('date', '<=', date_from), ('state', '=', 'done')],
            ['product_id', 'product_qty'],
            ['product_id'])
        moves_in = self.env['stock.move'].read_group(
            [('product_id', '=', product_id),
             ('location_dest_id', '=', location_id),
             ('date', '<=', date_from), ('state', '=', 'done')],
            ['product_id', 'product_qty'],
            ['product_id'])
        if moves_out:
            total_out = moves_out[0]['product_qty']
        if moves_in:
            total_in = moves_in[0]['product_qty']
        return total_in - total_out

    @api.model
    def get_lines(self):
        lines = []
        start_date = self.get_date_start() + ' 00:00:01'
        end_date = self.get_date_end() + ' 23:59:59'
        location = self.env.user.company_id.location_id.id
        if not location:
            raise ValidationError(
                _("Verify that a main warehouse is"
                  " configured for the report."))
        product_obj = self.env['product.product']
        stock_location_obj = self.env['stock.location']
        context = self.env.context
        dt_from = start_date
        data = self.do_query()
        for product_id, moves in data.items():
            domain_lines = []
            product = product_obj.browse(product_id)
            balance = 0
            date_from_str = start_date
            balance = self.get_initial_balance(
                product_id, date_from_str, location)
            lines.append({
                'id': 'product_%s' % (product_id),
                'name': product.name,
                'columns': (
                    [{'name': v} for v in [
                        product.uom_id.name, product.description, '%.2f' %
                        (sum([x['qty_done'] for x in moves]) + balance),
                        '$ ' + '%.2f' % product.list_price]]),
                'level': 2,
                'colspan': 4,
            })
        return lines

    @api.model
    def do_query(self):
        pp_obj = self.env['product.product']
        uom_obj = self.env['product.uom']
        results = {}
        tz = self._context.get('tz', 'America/Mexico_City')
        location_id = self.env.user.company_id.location_id.id
        if not location_id:
            raise ValidationError(
                _("Verify that a main warehouse is"
                  " configured for the report."))
        select = (
            """SELECT sml.product_id, sml.reference, sml.qty_done,
            sml.date AT TIME ZONE 'UTC' AT TIME ZONE %s AS date,
            sml.id, sml.location_id, sml.location_dest_id, sml.state,
            sml.product_uom_id
            FROM stock_move_line sml
            JOIN product_product pp ON pp.id = sml.product_id
            JOIN product_template pt ON pt.id = pp.product_tmpl_id
            WHERE sml.state = 'done' AND (
                sml.location_id = %s OR sml.location_dest_id = %s)
                AND sml.date AT TIME ZONE 'UTC' AT TIME ZONE %s >= %s
                AND sml.date AT TIME ZONE 'UTC' AT TIME ZONE %s <= %s
            """)
        select += "AND pt.product_brand = '%s'" % 'Rackmount'
        select += ' ORDER BY sml.date'
        start_date = self.get_date_start() + ' 00:00:01'
        end_date = self.get_date_end() + ' 23:59:59'
        self.env.cr.execute(
            select,
            (tz, location_id, location_id, tz, start_date, tz, end_date))
        query_data = self.env.cr.dictfetchall()
        for item in query_data:
            product = pp_obj.browse(item['product_id'])
            uom_id = uom_obj.browse(item['product_uom_id'])
            qty_done = uom_id._compute_quantity(
                item['qty_done'], product.uom_id)
            if item['product_id'] not in results.keys():
                results[item['product_id']] = []
            results[item['product_id']].append({
                'location_id': item['location_id'],
                'location_dest_id': item['location_dest_id'],
                'qty_done': (
                    qty_done if item['location_dest_id'] == location_id
                    else -qty_done),
                'date': item['date'],
                'move_id': item['id'],
                'move_name': item['reference'],
            })
        return results
