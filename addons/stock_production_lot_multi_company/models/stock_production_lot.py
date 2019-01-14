# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    def _default_company_id(self):
        company_model = self.env['res.company']
        return company_model._company_default_get('stock.production.lot')

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', change_default=True,
        default=_default_company_id)

    _sql_constraints = [
        ('name_ref_uniq_company', 'unique (name, product_id, company_id)',
         'The combination of serial number and product must be unique !'),
    ]

    @api.model_cr
    def init(self):
        """Remove the sql constrains that validate the code as unique """
        cr = self._cr
        cr.execute('''
            ALTER TABLE public.stock_production_lot
            DROP CONSTRAINT  IF EXISTS name_ref_uniq''')
