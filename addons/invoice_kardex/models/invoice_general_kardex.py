# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class InvoiceKardexGeneral(models.AbstractModel):
    _name = "invoice.kardex.general"
    _description = "General Ledger Report"
    _inherit = "invoice.kardex"

    filter_date = {
        'date_today': '',
        'filter': 'custom'}
    filter_partner = True
    filter_unfold_all = False

    def get_columns_name(self, options):
        return [
            {'name': _('Partner')},
            {'name': _('Date'), 'class': 'date'},
            {'name': _('Date Due'), 'class': 'date'},
            {'name': _('Days of credit'),
             'class': 'number',
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('Days of delay'),
             'class': 'number',
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('Up to date'),
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('30 days'),
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('60 days'),
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('90 days'),
             'style': 'text-align:center; white-space:nowrap;'},
            {'name': _('Messages')},
        ]

    @api.model
    def do_query(self, options, line_id=False):
        results = {}
        tz = self._context.get('tz', 'America/Mexico_City')
        select = (
            """SELECT ai.id, ai.residual, ai.number, ai.partner_id,
            ai.date AT TIME ZONE 'UTC' AT TIME ZONE %s AS date,
            ai.date_due AT TIME ZONE 'UTC' AT TIME ZONE %s AS date_due
            FROM account_invoice ai
            WHERE ai.residual != 0.0
            AND ai.type = 'out_invoice'
            AND ai.state = 'open'
            AND ai.company_id = %s
            """)
        if line_id:
            select += 'AND ai.partner_id = %s' % line_id
        if options.get('partner_ids'):
            select += 'AND ai.partner_id = %s' % options.get('partner_ids')[0]
        select += ' ORDER BY ai.date'
        if not options['date']['date_today']:
            options['date']['date_today'] = fields.Date.context_today(self)
        self.env.cr.execute(select, (tz, tz, self.env.user.company_id.id))
        query_data = self.env.cr.dictfetchall()
        for item in query_data:
            if item['partner_id'] not in results.keys():
                results[item['partner_id']] = []
            results[item['partner_id']].append({
                'residual': item['residual'],
                'number': item['number'],
                'date': item['date'],
                'date_due': item['date_due'],
                'invoice_id': item['id'],
            })
        return results

    @api.model
    def get_initial_balance(self, partner_id):
        invoices = self.env['account.invoice'].read_group(
            [('partner_id', '=', partner_id),
             ('state', '=', 'open')],
            ['partner_id', 'residual'],
            ['partner_id'])
        return invoices[0]['residual']

    @api.model
    def get_lines(self, options, line_id=None):
        lines = []
        partner_obj = self.env['res.partner']
        invoice_obj = self.env['account.invoice']
        context = self.env.context
        line_id = line_id and int(line_id.split('_')[1]) or None
        data = self.do_query(options, line_id)
        unfold_all = context.get('print_mode', False) and len(
            options.get('unfolded_lines')) == 0
        if context.get('print_mode', False):
            unfold_all = True
        for partner_id, invoices in data.items():
            domain_lines = []
            partner = partner_obj.browse(partner_id)
            balance = 0
            balance = self.get_initial_balance(partner_id)
            lines.append({
                'id': 'partner_%s' % (partner_id),
                'name': partner.name,
                'columns': (
                    [{'name': v} for v in [
                     ("TEL: " + partner.phone if partner.phone else ""),
                     ("Salesperson: " + partner.user_id.name
                      if partner.user_id else ""),
                     '$ ' + str(balance)]]),
                'level': 2,
                'unfoldable': True,
                'unfolded': 'partner_%s' % (
                    partner_id) in options.get('unfolded_lines') or unfold_all,
                'colspan': 7,
            })
            if 'partner_%s' % (
                    partner_id) in options.get(
                    'unfolded_lines') or unfold_all:
                for line in invoices:
                    invoice = invoice_obj.browse(line['invoice_id'])
                    days = (fields.Date.from_string(
                        fields.Date.context_today(self)) -
                        fields.Date.from_string(invoice.date_due)).days
                    days_of_credit = (
                        fields.Date.from_string(invoice.date_due) -
                        fields.Date.from_string(invoice.date)).days
                    message = invoice.message_ids.filtered(
                        lambda msg: msg.message_type == 'comment')
                    line_value = {
                        'id': line['invoice_id'],
                        'parent_id': 'partner_%s' % (partner_id),
                        'name': line['number'],
                        'columns': [{'name': v} for v in [
                            line['date'].strftime("%a, %d %B, %Y"),
                            line['date_due'].strftime("%a, %d %B, %Y"),
                            days_of_credit,
                            days if days > 0 else 0,
                            '$ ' + str(line['residual'] if days < 0 else 0.00),
                            '$ ' + str(
                                line['residual'] if days >= 1 and
                                days <= 30 else 0.00),
                            '$ ' + str(
                                line['residual'] if days >= 31 and
                                days <= 60 else 0.00),
                            '$ ' + str(
                                line['residual'] if days >= 61 else 0.00),
                            message[0].body.replace(
                                '<p>', '').replace(
                                '</p>', '') if message else _("No message"),
                        ]],
                        'level': 4,
                        'caret_options': 'account.invoice',
                    }
                    domain_lines.append(line_value)
                lines += domain_lines
        return lines

    @api.model
    def get_report_name(self):
        return _("Customers")
