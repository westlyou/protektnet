# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class InvoiceKardexGeneral(models.AbstractModel):
    _name = "invoice.kardex.general"
    _description = "General Ledger Report"
    _inherit = "invoice.kardex"

    filter_date = {
        'date_from': '',
        'date_to': '',
        'filter': 'custom'}
    filter_product = True
    filter_brand = True
    filter_unfold_all = False

    def get_columns_name(self, options):
        return [
            {'name': '' if not self._context.get('print_mode', False) else _("Product")},
            {'name': _("Type")if not self._context.get('print_mode', False) else ""},
            {'name': (_("Date") if not self._context.get('print_mode', False) else ""), 'class': 'date'},
            {'name': (_("Quantity") if not self._context.get('print_mode', False) else ""), 'class': 'number'},
            {'name': _("UoM")},
            {'name': "" if not self._context.get('print_mode', False) else _("Description")},
            {'name': _("Stock"), 'class': 'number'},
            {'name': _("MSRP"), 'class': 'number'},
        ]

    @api.model
    def do_query(self, options, line_id=False):
        pp_obj = self.env['product.product']
        uom_obj = self.env['product.uom']
        results = {}
        context = self.env.context
        tz = self._context.get('tz', 'America/Mexico_City')
        location_id = 82
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
        if line_id:
            select += 'AND sml.product_id = %s' % line_id
        elif context.get('filter_product_ids') and len(
                context['filter_product_ids'].ids) > 1:
            select += 'AND sml.product_id IN %s' % (tuple(
                context['filter_product_ids'].ids), )
        elif context.get('filter_product_ids') and len(
                context['filter_product_ids'].ids) == 1:
            select += 'AND sml.product_id = %s' % context[
                'filter_product_ids'].id
        elif context.get('filter_brand_ids') and len(
                context['filter_brand_ids']) > 1:
            select += 'AND pt.product_brand IN %s' % (tuple(
                context['filter_brand_ids']), )
        elif context.get('filter_brand_ids') and len(
                context['filter_brand_ids']) == 1:
            select += "AND pt.product_brand = '%s'" % context[
                'filter_brand_ids'][0]
        select += ' ORDER BY sml.date'
        if not options['date']['date_from'] or not options['date']['date_to']:
            options['date']['date_from'] = self.get_date_start()
            options['date']['date_to'] = self.get_date_end()
        start_date = options['date']['date_from'] + ' 00:00:01'
        end_date = options['date']['date_to'] + ' 23:59:59'
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
    def get_lines(self, options, line_id=None):
        lines = []
        location = 82
        if not location:
            raise ValidationError(
                _("Verify that a main warehouse is"
                  " configured for the report."))
        product_obj = self.env['product.product']
        stock_location_obj = self.env['stock.location']
        context = self.env.context
        dt_from = options['date'].get('date_from')
        line_id = line_id and int(line_id.split('_')[1]) or None
        data = self.with_context(
            date_from_aml=dt_from,
            date_from=dt_from).do_query(options, line_id)
        unfold_all = context.get('print_mode', False) and len(
            options.get('unfolded_lines')) == 0
        for product_id, moves in data.items():
            domain_lines = []
            product = product_obj.browse(product_id)
            balance = 0
            date_from_str = options['date']['date_from']
            balance = self.get_initial_balance(
                product_id, date_from_str, location)
            lines.append({
                'id': 'product_%s' % (product_id),
                'name': product.name,
                'columns': (
                    [{'name': v} for v in [
                        product.uom_id.name, "" if not self.env.context.get('print_mode', False) else product.description, '%.2f' %
                        (sum([x['qty_done'] for x in moves]) + balance),
                        '$ ' + '%.2f' % product.list_price]]),
                'level': 2,
                'unfoldable': True,
                'unfolded': 'product_%s' % (
                    product_id) in options.get('unfolded_lines') or unfold_all,
                'colspan': 4,
            })
            if not self.env.context.get('print_mode', False):
                if 'product_%s' % (
                        product_id) in options.get(
                        'unfolded_lines') or unfold_all:
                    domain_lines = [{
                        'id': 'initial_%s' % (product_id),
                        'class': 'o_invoice_reports_initial_balance',
                        'name': _('Initial Balance'),
                        'parent_id': 'product_%s' % (product_id),
                        'columns': [{'name': v} for v in ['%.2f' % balance]],
                        'level': 4,
                        'colspan': 5,
                    }]
                    for line in moves:
                        location_id = stock_location_obj.browse(
                            line['location_id'])
                        location_dest_id = stock_location_obj.browse(
                            line['location_dest_id'])
                        balance += line['qty_done']
                        line_value = {
                            'id': line['move_id'],
                            'parent_id': 'product_%s' % (product_id),
                            'name': line['move_name'],
                            'columns': [{'name': v} for v in [
                                'IN <-- %s' % location_id.name if
                                line['location_dest_id'] == location
                                else 'OUT --> %s' %
                                location_dest_id.name,
                                line['date'], "", '%.2f' % line[
                                    'qty_done'], '', '%.2f' % balance, '']],
                            'level': 4,
                            'caret_options': 'stock.move.line',
                        }
                        domain_lines.append(line_value)
                    lines += domain_lines
        return lines

    @api.model
    def get_report_name(self):
        return _("Customers")
