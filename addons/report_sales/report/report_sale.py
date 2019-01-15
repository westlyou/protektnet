# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError


class ReportSalekardex(models.AbstractModel):
    _name = 'report.report_sales.report_sale'

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = self._context.get('active_model')
        docs = self.env[self.model].browse(self._context.get('active_id'))
        sol = self.env['sale.order.line']
        domain = [
            ('order_id.date_order', '>=', docs.start_date),
            ('order_id.date_order', '<=', docs.end_date),
            ('company_id', '=', self.env.user.company_id.id),
            ('state', '=', 'sale'),
        ]
        if docs.product_brand != 'all':
            domain.append(
                ('product_id.product_tmpl_id.x_studio_field_U36cw', '=',
                    docs.product_brand))
        if docs.licenses and docs.serials:
            domain.append(
                ('product_id.categ_id', 'in', [4, 5]))
        if docs.licenses and not docs.serials:
            domain.append(
                ('product_id.categ_id', 'in', [5]))
        if not docs.licenses and docs.serials:
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
                'product_uom_qty': so_line.get('product_uom_qty'),
                'total': so_line.get('price_subtotal'),
            })
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'time': time,
            'products': sorted_product_records
        }
