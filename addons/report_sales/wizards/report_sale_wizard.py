# Copyright 2019 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import calendar
from datetime import datetime

from odoo import _, api, fields, models


class ReportSaleWizard(models.TransientModel):
    _name = "report.sale.wizard"

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

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = (self.read([
            'start_date', 'end_date', 'licenses',
            'serials', 'product_brand'])[0])
        return self.env.ref(
            'report_sales.action_report_sale').report_action(
            self, data=data, config=False)
