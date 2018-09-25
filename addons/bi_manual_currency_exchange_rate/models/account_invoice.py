# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api
from odoo.exceptions import UserError

class account_invoice_line(models.Model):
    _inherit ='account.invoice.line'
    print("inside account_invoice_line-----------")
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.invoice_id:
            return
        if self.invoice_id.manual_currency_rate_active:
            manual_currency_rate = self.product_id.lst_price * self.invoice_id.manual_currency_rate
            self.price_unit = manual_currency_rate
            self.name = self.product_id.name
        if self.invoice_id.manual_currency_rate_active is False:
            manual_currency_rate = self.product_id.lst_price
            self.price_unit = manual_currency_rate
            self.name = self.product_id.name
        
class account_invoice(models.Model):
    _inherit ='account.invoice'
    print("------------- Inside account invoice ----------------------")
    manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
    manual_currency_rate = fields.Float('Rate', digits=(12, 6))

    @api.multi
    def action_move_create(self):
        """ Creates invoice related analytics and financial move lines """
        account_move = self.env['account.move']
        price = False
        for inv in self:
            if not inv.journal_id.sequence_id:
                raise UserError(_('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line_ids:
                raise UserError(_('Please create some invoice lines.'))
            if inv.move_id:
                continue

            ctx = dict(self._context, lang=inv.partner_id.lang)
            if not inv.date_invoice:
                inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
            date_invoice = inv.date_invoice
            company_currency = inv.company_id.currency_id

            # create move lines (one per invoice line + eventual taxes and analytic lines)
            iml = inv.invoice_line_move_line_get()
            iml += inv.tax_line_move_line_get()

            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)
#            if inv.manual_currency_rate_active:
#                for i in iml:
#                    print "\n \n ====================================iml",i
#                    price = i.get('amount_currency') / inv.manual_currency_rate
#                    if i.get('price') > 0:
#                        i.update({'price':price})
#                    else:
#                        i.update({'price':-price})
            name = inv.name or '/'
            if inv.payment_term_id:
                totlines = inv.with_context(ctx).payment_term_id.with_context(currency_id=company_currency.id).compute(total, date_invoice)[0]
                res_amount_currency = total_currency
                ctx['date'] = date_invoice
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency
                    if inv.manual_currency_rate_active:
#                        if t[1] < 0:
#                            price = -price
                        iml.append({
                            'type': 'dest',
                            'name': name,
                            'price': price,
                            'account_id': inv.account_id.id,
                            'date_maturity': t[0],
                            'amount_currency': diff_currency and amount_currency,
                            'currency_id': diff_currency and inv.currency_id.id,
                            'invoice_id': inv.id
                        })
                    else:
                        iml.append({
                            'type': 'dest',
                            'name': name,
                            'price': t[1],
                            'account_id': inv.account_id.id,
                            'date_maturity': t[0],
                            'amount_currency': diff_currency and amount_currency,
                            'currency_id': diff_currency and inv.currency_id.id,
                            'invoice_id': inv.id
                        })
            else:
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': price if price else total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'invoice_id': inv.id
                })
            if inv.manual_currency_rate_active:
                for i in iml:
                    price = i.get('amount_currency') / inv.manual_currency_rate
                    if i.get('price') > 0 or i.get('type') == 'dest':
                        i.update({'price':price})
                    else:
                        i.update({'price':-price})
            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
            line = [(0, 0, self.line_get_convert(l, part.id)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            line = inv.finalize_invoice_move_lines(line)
            date = inv.date or date_invoice
            move_vals = {
                'ref': inv.reference,
                'line_ids': line,
                'journal_id': journal.id,
                'date': date,
                'narration': inv.comment,
            }
            ctx['company_id'] = inv.company_id.id
            ctx['invoice'] = inv
            ctx_nolang = ctx.copy()
            ctx_nolang.pop('lang', None)
            move = account_move.with_context(ctx_nolang).create(move_vals)
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            move.post()
            # make the invoice point to that move
            vals = {
                'move_id': move.id,
                'date': date,
                'move_name': move.name,
            }
            inv.with_context(ctx).write(vals)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
