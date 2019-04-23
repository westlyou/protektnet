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
    filter_partners = True
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
            """SELECT ai.id, ai.residual_company_signed, ai.number,
            ai.partner_id,
            ai.date AT TIME ZONE 'UTC' AT TIME ZONE %s AS date,
            ai.date_due AT TIME ZONE 'UTC' AT TIME ZONE %s AS date_due,
            ai.currency_id AS currency
            FROM account_invoice ai
            WHERE ai.residual_company_signed != 0.0
            AND ai.type = 'out_invoice'
            AND ai.state = 'open'
            AND ai.company_id = %s
            """)
        if line_id:
            select += 'AND ai.partner_id = %s' % line_id
        # if options.get('partners'):
        #     partners = [p.get('id') for p in options.get('partners') if
        #                 p.get('selected')]
        #     if partners:
        #         if len(partners) == 1:
        #             select += 'AND ai.partner_id = %s' % partners[0]
        #         else:
        #             select += 'AND ai.partner_id in %s' % tuple(partners)
        select += ' ORDER BY ai.date'
        if not options['date']['date_today']:
            options['date']['date_today'] = fields.Date.context_today(self)
        self.env.cr.execute(select, (tz, tz, self.env.user.company_id.id))
        query_data = self.env.cr.dictfetchall()
        for item in query_data:
            if item['partner_id'] not in results.keys():
                results[item['partner_id']] = []
            results[item['partner_id']].append({
                'residual_company_signed': item['residual_company_signed'],
                'number': item['number'],
                'date': item['date'],
                'date_due': item['date_due'],
                'invoice_id': item['id'],
                'currency': item['currency']
            })
        return results

    @api.model
    def get_initial_balance(self, partner_id):
        invoices = self.env['account.invoice'].read_group(
            [('partner_id', '=', partner_id),
             ('state', '=', 'open')],
            ['partner_id', 'residual_company_signed'],
            ['partner_id'])
        return invoices[0]['residual_company_signed']

    def addComa(self, snum):
        s = snum
        i = s.index('.')
        while i > 3:
            i = i - 3
            s = s[:i] + ',' + s[i:]
        return s

    def get_initial_dates(self, invoice):
        sale = self.env['sale.order'].search([('name', '=', invoice.origin)])
        if (len(sale.invoice_ids.filtered(
                lambda inv: inv.state != 'cancel')) == 1 or
                'out_refund' not in sale.invoice_ids.mapped('type')):
            return invoice.date, invoice.date_due
        else:
            inv_refund = sale.invoice_ids.filtered(
                lambda inv: inv.state != 'cancel' and inv.state == 'paid' and
                inv.type == 'out_invoice')
            date_due = (inv_refund.date_due if inv_refund.date_due else
                        inv_refund.date)
            return inv_refund.date, date_due

    @api.model
    def get_lines(self, options, line_id=None):
        lines = []
        partner_obj = self.env['res.partner']
        invoice_obj = self.env['account.invoice']
        usd = self.env['res.currency'].browse(3)
        mxn = self.env['res.currency'].browse(34)
        context = self.env.context
        line_id = line_id and int(line_id.split('_')[1]) or None
        data = self.do_query(options, line_id)
        unfold_all = context.get('print_mode', False) and len(
            options.get('unfolded_lines')) == 0
        if context.get('print_mode', False):
            unfold_all = True
        for partner_id, invoices in data.items():
            domain_lines = []
            currencys = [inv.get('currency') for inv in invoices]
            no_dolar = (34 in currencys and len(set(currencys)) == 1)
            amount = self.get_initial_balance(partner_id)
            partner = partner_obj.browse(partner_id)
            balance = (
                'MXN: ' + self.addComa('%.2f' % (amount)) +
                ' - USD: ' + self.addComa('%.2f' % (mxn.compute(amount, usd)))
            ) if not no_dolar else 'MXN: ' + self.addComa('%.2f' % (amount))
            lines.append({
                'id': 'partner_%s' % (partner_id),
                'name': partner.name,
                'columns': (
                    [{'name': v} for v in [
                     ("TEL: " + partner.phone if partner.phone else ""),
                     ("Salesperson: " + partner.user_id.name
                      if partner.user_id else ""), balance]]),
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
                    start_date, end_date = self.get_initial_dates(invoice)
                    days = (fields.Date.from_string(
                        fields.Date.context_today(self)) -
                        fields.Date.from_string(end_date)).days
                    days_of_credit = (
                        fields.Date.from_string(end_date) -
                        fields.Date.from_string(start_date)).days
                    message = invoice.message_ids.filtered(
                        lambda msg: msg.message_type == 'comment')
                    amount_line = line['residual_company_signed']
                    value = (
                        'MXN: ' + self.addComa('%.2f' % (amount_line)) +
                        ' - USD: ' + self.addComa(
                            '%.2f' % (mxn.compute(amount_line, usd)))
                    ) if not no_dolar else 'MXN: ' + self.addComa(
                        '%.2f' % (amount_line))
                    line_value = {
                        'id': line['invoice_id'],
                        'parent_id': 'partner_%s' % (partner_id),
                        'name': (
                            line['number'] + '-' + invoice.currency_id.name),
                        'columns': [{'name': v} for v in [
                            fields.Date.from_string(start_date).strftime(
                                "%a, %d %B, %Y"),
                            fields.Date.from_string(end_date).strftime(
                                "%a, %d %B, %Y"),
                            days_of_credit,
                            days if days > 0 else 0,
                            value if days < 0 else '0.00',
                            value if days >= 1 and days <= 30 else '0.00',
                            value if days >= 31 and days <= 60 else '0.00',
                            value if days >= 61 else '0.00',
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

    @api.model
    def get_report_rate(self):
        usd = self.env['res.currency'].browse(3)
        rate = 0.00
        rates = usd.rate_ids.filtered(
            lambda usd: usd.company_id == usd.env.user.company_id)
        if rates:
            rate = 1 / rates[0].rate
        return rate
