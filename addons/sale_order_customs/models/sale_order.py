# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_count = fields.Integer(
        string='Purchases',
        compute='_compute_purchase_count'
    )
    state = fields.Selection(selection_add=[('consignment', 'Consignment')])
    consignment = fields.Boolean(
        string='Consignment',
        compute="_compute_consignment",
        store=True,
    )
    quote = fields.Char(string='Quote Number')
    deal = fields.Char(string='Deal Registration')

    @api.depends('picking_ids')
    def _compute_consignment(self):
        for rec in self:
            rec.consignment = bool(rec.picking_ids.filtered(
                lambda x: x.state not in ['draft', 'cancel']
            ).mapped('owner_id'))
            if rec.consignment:
                rec.write({'state': 'consignment'})

    @api.multi
    def action_invoice_consignment(self):
        for rec in self:
            rec.state = 'sale'
            rec.consignment = False

    @api.depends('order_line')
    def _compute_purchase_count(self):
        for rec in self:
            pos = self.env['purchase.order.line'].search([
                ('sale_line_id', 'in',
                    rec.mapped('order_line').ids)]).mapped('order_id')
            rec.purchase_count = len(pos)

    @api.multi
    def action_view_purchase(self):
        context = dict(self._context or {})
        pos = self.env['purchase.order.line'].search([
            ('sale_line_id', 'in',
                self.mapped('order_line').ids)]).mapped('order_id')
        return {
            'name': _('Purchase Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', pos.ids)],
            'context': context,
        }

    # @api.multi
    # def action_invoice_create(self, grouped=False, final=False):
    #     res = super(SaleOrder, self).action_invoice_create(
    #         grouped, final)
    #     if self.auto_purchase_order_id:
    #         self.create_invoice(self.auto_purchase_order_id)
    #     return res

    # @api.model
    # def prepare_lines(self, product, quantity, price_unit, tax,
    #                   account, line, company):
    #     return {
    #         'product_id': product.id,
    #         'quantity': quantity,
    #         'price_unit': price_unit,
    #         'uom_id': product.uom_id.id,
    #         'invoice_line_tax_ids': [(6, 0, [x.id for x in tax])],
    #         'name': product.name,
    #         'account_id': account.id,
    #         'purchase_line_id': line.id,
    #         'company_id': company.id,
    #     }

    # @api.multi
    # def create_invoice(self, purchase):
    #     lines = []
    #     company_rec = self.env['res.company']._find_company_from_partner(
    #         self.partner_id.id)
    #     obj_invoice = self.env['account.invoice']
    #     res = self.prepare_invoice(purchase, lines, company_rec)
    #     currency_id = self.sudo().auto_purchase_order_id.currency_id.id
    #     intercompany_uid = (
    #         company_rec.intercompany_user_id and
    #         company_rec.intercompany_user_id.id or False)
    #     obj_invoice.sudo(
    #         intercompany_uid).create({
    #             'origin': purchase.sudo().name,
    #             'reference': 'Invoice of SO',
    #             'partner_id': res['partner_id'].id,
    #             'fiscal_position_id': res['fpos'].id,
    #             'currency_id': currency_id,
    #             'account_id': res['invoice_account'].id,
    #             'type': res['invoice_type'],
    #             'company_id': company_rec.id,
    #             'purchase_id': purchase.sudo().id,
    #             'invoice_line_ids': [line for line in res['lines']],
    #         })

    # @api.model
    # def prepare_invoice(self, purchase, lines, company):
    #     res = {}
    #     res['invoice_type'] = 'in_invoice'
    #     partner_id = purchase.sudo().partner_id
    #     res['partner_id'] = partner_id
    #     fpos = partner_id.property_account_position_id
    #     res['fpos'] = fpos
    #     res['invoice_account'] = fpos.map_account(
    #         partner_id.property_account_payable_id)
    #     for line in purchase.sudo().order_line:
    #         if line.product_id.property_account_expense_id:
    #             account = line.property_account_expense_id
    #         elif (line.product_id.categ_id.
    #               property_stock_account_input_categ_id):
    #             account = (
    #                 line.product_id.categ_id.
    #                 property_stock_account_input_categ_id)
    #         tax = fpos.map_tax(
    #             line.product_id.supplier_taxes_id.with_context(
    #                 company=company).filtered(
    #                 lambda x: x.company_id == x._context.get('company')))
    #         lines.append(
    #             (0, 0, self.prepare_lines
    #                 (line.product_id, line.product_qty,
    #                  line.price_unit, tax, account, line, company)))
    #     res['lines'] = lines
    #     return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    serial_numbers = fields.Char(
        string='Serial Numbers',
    )
