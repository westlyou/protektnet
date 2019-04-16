# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
from datetime import datetime
import io
import lxml.html
from odoo import _, api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, config, pycompat
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import safe_eval

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

_logger = logging.getLogger(__name__)


class InvoiceKardexManager(models.Model):
    _name = 'invoice.kardex.manager'

    report_name = fields.Char(
        required=True, help='name of the model of the report')


class InvoiceKardex(models.AbstractModel):
    _name = 'invoice.kardex'

    filter_date = None
    filter_partner = None
    filter_unfold_all = None
    filter_hierarchy = None

    def _build_options(self, previous_options=None):
        if not previous_options:
            previous_options = {}
        options = {}
        filter_list = [attr for attr in dir(self) if
                       attr.startswith('filter_') and
                       len(attr) > 7 and not callable(getattr(self, attr))]
        for element in filter_list:
            filter_name = element[7:]
            options[filter_name] = getattr(self, element)
        if options.get('partner'):
            options['partner'] = self.get_partners()

        options['unfolded_lines'] = []
        for key, value in options.items():
            if(key in previous_options and value is not None and
                    previous_options[key] is not None):
                if key == 'date':
                    options[key]['filter'] = 'custom'
                    if (value.get('date_from') is not None and not
                            previous_options[key].get('date_from')):
                        options[key]['date_from'] = self.get_date_start
                        options[key]['date_to'] = self.get_date_end
                    elif value.get(
                            'date') is not None and not previous_options[
                                key].get('date'):
                        options[key]['date'] = previous_options[key]['date_to']
                    else:
                        options[key] = previous_options[key]
                else:
                    options[key] = previous_options[key]
        return options

    # TO BE OVERWRITTEN
    def get_columns_name(self, options):
        return []

    # TO BE OVERWRITTEN
    def get_lines(self, options, line_id=None):
        return []

    # TO BE OVERWRITTEN
    def get_templates(self):
        return {
            'main_template': 'invoice_kardex.main_template',
            'line_template': 'invoice_kardex.line_template',
            'footnotes_template': 'invoice_kardex.footnotes_template',
            'search_template': 'invoice_kardex.search_template',
        }

    # TO BE OVERWRITTEN
    def get_report_name(self):
        return _('Invoice Kardex')

    @api.model
    def get_options(self, previous_options=None):
        if self.filter_partner:
            self.filter_partner_ids = [] if self.filter_partner else None
        return self._build_options(previous_options)

    def get_report_filename(self, options):
        return self.get_report_name().lower().replace(' ', '_')

    def execute_action(self, options, params=None):
        # Verificar funcionamiento de este metodo si no es necesario
        # borrarlo.
        action_id = int(params.get('actionId'))
        action = self.env['ir.actions.actions'].browse([action_id])
        action_type = action.type
        action = self.env[action.type].browse([action_id])
        action_read = action.read()[0]
        if action_type == 'ir.actions.client':
            if action.tag == 'invoice_report':
                options['unfolded_lines'] = []
                options['unfold_all'] = False
                another_report_context = safe_eval(action_read['context'])
                another_report = self.browse(another_report_context['id'])
                if not self.date_range and another_report.date_range:
                    options['date'].pop('filter')
                action_read.update(
                    {'options': options, 'ignore_session': 'read'})
        if params.get('id'):
            context = action_read.get('context') and safe_eval(
                action_read['context']) or {}
            context.setdefault('active_id', int(params['id']))
            action_read['context'] = context
        return action_read

    @api.multi
    def open_account_invoice(self, options, params=None):
        if not params:
            params = {}
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': params.get('id', False),
            'views': [(False, 'form')],
            'target': 'self',
        }

    def set_context(self, options):
        ctx = self.env.context.copy()
        if options.get('date') and options['date'].get('date_today'):
            ctx['date_today'] = options['date']['date_today']
        if options.get('partner_ids'):
            ctx['filter_partner_ids'] = self.env[
                'res.partner'].browse(
                    [int(acc) for acc in options['partner_ids']])
        return ctx

    @api.multi
    def get_report_informations(self, options):
        options = self.get_options(options)

        searchview_dict = {'options': options, 'context': self.env.context}
        # Check if report needs analytic
        if options.get('partner') is not None:
            searchview_dict['partner_ids'] = ([
                (t.id, t.name) for t in
                self.env['res.partner'].search([])] or False)
        report_manager = self.get_report_manager(options)
        info = {'options': options,
                'context': self.env.context,
                'report_manager_id': report_manager.id,
                'footnotes': '',
                'buttons': self.get_reports_buttons(),
                'main_html': self.get_html(options),
                'searchview_html': self.env['ir.ui.view'].render_template(
                    self.get_templates().get(
                        'search_template',
                        'invoice_kardex.search_template'),
                    values=searchview_dict),
                }
        return info

    @api.multi
    def get_html(self, options, line_id=None, additional_context=None):
        templates = self.get_templates()
        report = {'name': self.get_report_name(),
                  'company_name': self.env.user.company_id.name}
        lines = self.with_context(
            self.set_context(options)).get_lines(options, line_id=line_id)
        rcontext = {
            'report': report,
            'lines': {'columns_header': self.get_columns_name(options),
                      'lines': lines},
            'options': options,
            'context': self.env.context,
            'model': self,
        }
        if additional_context and type(additional_context) == dict:
            rcontext.update(additional_context)
        render_template = templates.get(
            'main_template', 'invoice_kardex.main_template')
        if line_id is not None:
            render_template = templates.get(
                'line_template', 'invoice_kardex.line_template')
        html = self.env['ir.ui.view'].render_template(
            render_template,
            values=dict(rcontext),
        )
        if self.env.context.get('print_mode', False):
            for k, v in self.replace_class().items():
                html = html.replace(k, v)
            html = html.replace(
                b'<div class="js_invoice_report_footnotes"></div>',
                self.get_html_footnotes(''))
        return html

    @api.multi
    def get_html_footnotes(self, footnotes):
        template = self.get_templates().get(
            'footnotes_template', 'invoice_kardex.footnotes_template')
        rcontext = {'footnotes': footnotes, 'context': self.env.context}
        html = self.env['ir.ui.view'].render_template(
            template, values=dict(rcontext))
        return html

    def get_reports_buttons(self):
        return [
            {'name': _('Print Preview'), 'action': 'print_pdf'},
            {'name': _('Export (XLSX)'), 'action': 'print_xlsx'}]

    def get_report_manager(self, options):
        domain = [('report_name', '=', self._name)]
        selected_companies = []
        if options.get('multi_company'):
            selected_companies = [c['id'] for c in options['multi_company']
                                  if c.get('selected')]
        if len(selected_companies) == 1:
            domain += [('company_id', '=', selected_companies[0])]
        existing_manager = self.env['invoice.kardex.manager'].search(
            domain, limit=1)
        return existing_manager

    def _get_filter_partner(self):
        return self.env['res.partner'].search([
            ('company_id', '=', self.env.user.company_id.id)])

    def get_partners(self):
        partner_read = self._get_filter_partner()
        partners = []
        for c in partner_read:
            partners.append({
                'id': c.id,
                'name': c.name,
                'selected': False,
            })
        return partners

    def format_date(self, dt_to, dt_from, options, dt_filter='date'):
        if isinstance(dt_to, pycompat.string_types):
            dt_to = datetime.strptime(dt_to, DEFAULT_SERVER_DATE_FORMAT)
        if dt_from and isinstance(dt_from, pycompat.string_types):
            dt_from = datetime.strptime(dt_from, DEFAULT_SERVER_DATE_FORMAT)
        if not dt_from:
            return _('As of %s') % (format_date(self.env, dt_to.strftime(
                DEFAULT_SERVER_DATE_FORMAT)),)
        return _('From %s <br/> to  %s') % (
            format_date(self.env, dt_from.strftime(
                DEFAULT_SERVER_DATE_FORMAT)), format_date(
                self.env, dt_to.strftime(DEFAULT_SERVER_DATE_FORMAT)))

    def print_pdf(self, options):
        return {
            'type': 'ir_actions_invoice_report_download',
            'data': {
                'model': self.env.context.get('model'),
                'options': json.dumps(options),
                'output_format': 'pdf',
                'invoice_kardex_id': self.env.context.get('id'),
            }
        }

    def replace_class(self):
        return {
            b'o_invoice_reports_no_print': b'',
            b'table-responsive': b'',
            b'<a': b'<span',
            b'</a>': b'</span>'
        }

    def get_pdf(self, options, minimal_layout=True):
        if not config['test_enable']:
            self = self.with_context(commit_assetsbundle=True)

        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'report.url') or self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
        rcontext = {
            'mode': 'print',
            'base_url': base_url,
            'company': self.env.user.company_id,
        }

        body = self.env['ir.ui.view'].render_template(
            "invoice_kardex.print_template",
            values=dict(rcontext),
        )
        body_html = self.with_context(
            print_mode=True).get_html(options)

        body = body.replace(
            b'<body class="o_invoice_reports_body_print">',
            b'<body class="o_invoice_reports_body_print">' + body_html)
        if minimal_layout:
            header = self.env['ir.actions.report'].render_template(
                "invoice_kardex.internal_layout_invoice_kardex",
                values=rcontext)
            footer = ""
            spec_paperformat_args = {
                'data-report-margin-top': 15,
                'data-report-header-spacing': 15}
            header = self.env['ir.actions.report'].render_template(
                "web.minimal_layout",
                values=dict(rcontext, subst=True, body=header))
        else:
            rcontext.update({
                'css': '',
                'o': self.env.user,
                'res_company': self.env.user.company_id,
            })
            header = self.env['ir.actions.report'].render_template(
                "web.external_layout", values=rcontext)
            header = header.decode('utf-8')
            spec_paperformat_args = {}
            try:
                root = lxml.html.fromstring(header)
                match_klass = (
                    "//div[contains(concat(' ', normalize-space(@class), " +
                    "' '), ' {} ')]")

                for node in root.xpath(match_klass.format('header')):
                    headers = lxml.html.tostring(node)
                    headers = self.env['ir.actions.report'].render_template(
                        "web.minimal_layout", values=dict(
                            rcontext, subst=True, body=headers))

                for node in root.xpath(match_klass.format('footer')):
                    footer = lxml.html.tostring(node)
                    footer = self.env['ir.actions.report'].render_template(
                        "web.minimal_layout", values=dict(
                            rcontext, subst=True, body=footer))

            except lxml.etree.XMLSyntaxError:
                headers = header
                footer = ''
            header = headers

        landscape = False
        if len(self.with_context(
                print_mode=True).get_columns_name(options)) > 5:
            landscape = True

        return self.env['ir.actions.report']._run_wkhtmltopdf(
            [body],
            header=header, footer=footer,
            landscape=landscape,
            specific_paperformat_args=spec_paperformat_args
        )

    def print_xlsx(self, options):
        return {
            'type': 'ir_actions_invoice_report_download',
            'data': {
                'model': self.env.context.get('model'),
                'options': json.dumps(options),
                'output_format': 'xlsx',
                'invoice_kardex_id': self.env.context.get('id'),
            }
        }

    def get_xlsx(self, options, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(self.get_report_name()[:31])

        title_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2})
        level_2_style = workbook.add_format({
            'font_name': 'Arial',
            'bold': False,
            'top': 2,
            'align': 'right',
        })
        level_2_style.set_text_wrap()
        level_2_style_right = workbook.add_format({
            'font_name': 'Arial',
            'bold': False,
            'top': 2,
            'right': 2})
        level_2_style_right.set_bg_color('#808080')
        upper_line_style = workbook.add_format({
            'font_name': 'Arial', 'top': 2})

        sheet.set_column(0, 0, 15)
        sheet.write(0, 0, '', title_style)

        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        merge_total = workbook.add_format({
            'bold': 1,
            'align': 'right',
            'valign': 'vright',
        })
        merge_total.set_bg_color('#808080')
        sheet.merge_range('A1:I1', self.env.user.company_id.name, merge_format)
        sheet.merge_range(
            'A2:I2', _("Summary of due accounts receivable"),
            merge_format)
        sheet.merge_range('A3:I3', "Al " + fields.Date.from_string(
            fields.Date.today()).strftime("%a, %d %B, %Y"), merge_format)
        x = 0
        y_offset = 3
        for column in [x for x in self.with_context(
                print_mode=True).get_columns_name(
                options) if len(x['name']) > 1]:
            sheet.write(
                y_offset, x,
                column.get('name', '').replace(
                    '<br/>', ' ').replace('&nbsp;', ' '), title_style)
            x += 1
        y_offset += 1
        ctx = self.set_context(options)
        ctx.update({'print_mode': True})
        lines = self.with_context(ctx).get_lines(options)
        if lines:
            max_width = max([len(l['columns']) for l in lines])
        sheet.set_column('J:J', 40)
        sheet.set_column('B:B', 23)
        sheet.set_column('C:C', 23)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        for y in range(0, len(lines)):
            if lines[y].get('level') == 2:
                style = level_2_style_right
            else:
                style = level_2_style
            sheet.write(y + y_offset, 0, lines[y]['name'], style)
            for x in range(1, max_width - len(lines[y]['columns']) + 1):
                sheet.write(y + y_offset, x, None, style)
            for x in range(1, len(lines[y]['columns']) + 1):
                if (lines[y].get('level') == 2 and
                    lines[y].get('colspan') == 8 and
                        lines[y]['columns'][x - 1].get('name', '')):
                    if '$' in lines[y]['columns'][x - 1].get('name', ''):
                        sheet.merge_range(
                            'G' + str(y + y_offset + 1) + ':J' +
                            str(y + y_offset + 1),
                            lines[y]['columns'][x - 1].get('name', ''),
                            merge_total)
                    else:
                        sheet.merge_range(
                            'B' + str(y + y_offset + 1) + ':F' +
                            str(y + y_offset + 1),
                            lines[y]['columns'][x - 1].get('name', ''),
                            merge_total)
                else:
                    sheet.write(
                        y + y_offset,
                        x, lines[y][
                            'columns'][x - 1].get('name', ''), style)

        if lines:
            for x in range(max_width + 1):
                sheet.write(len(lines) + y_offset, x, None, upper_line_style)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
