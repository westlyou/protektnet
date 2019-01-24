# -*- coding: utf-8 -*-
# © <2019> <Grupo Censere>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'product.template'

    # product_brand = fields.Selection([
    #     ('Airtight', 'Airtight'), ('Barracuda', 'Barracuda'),
    #     ('Bitdefender', 'Bitdefender'), ('Bugooro', 'Bugooro'),
    #     ('Cautio', 'Cautio'), ('Consulting', 'Consulting'),
    #     ('Cyberoam', 'Cyberoam'), ('EndPoint', 'EndPoint'),
    #     ('Expand', 'Expand'), ('FatPipe', 'FatPipe'),
    #     ('GrandStream', 'GrandStream'), ('HanDreamNet', 'HanDreamNet'),
    #     ('Hauri', 'Hauri'), ('Infoblox', 'Infoblox'),
    #     ('InterGuard', 'InterGuard'), ('IP Guard', 'IP Guard'),
    #     ('IP Scan', 'IP Scan'), ('Juniper', 'Juniper'),
    #     ('LogRhythm', 'LogRhythm'), ('Lok-it', 'Lok-it'),
    #     ('LUMEN CACHE', 'LUMEN CACHE'), ('M86', 'M86'),
    #     ('Mykonos', 'Mykonos'), ('NCP', 'NCP'), ('nProtect', 'nProtect'),
    #     ('Okiok', 'Okiok'), ('otros', 'otros'), ('Portafolio', 'Portafolio'),
    #     ('Rackmount', 'Rackmount'), ('Remote Call', 'Remote Call'),
    #     ('Servicios', 'Servicios'), ('Somansa', 'Somansa'),
    #     ('Sophos', 'Sophos'), ('Spamina', 'Spamina'),
    #     ('Spector', 'Spector'), ('Terranova', 'Terranova')],
    #     string="Brand",
    #     store=True,
    #     compute="_compute_product_brand")
    long_product = fields.Integer(string='Long', )
    width_product = fields.Integer(string='Width', )
    high_product = fields.Integer(string='Higt', )

    # @api.depends('x_studio_field_U36cw')
    # def _compute_product_brand(self):
    #     for rec in self:
    #         rec.product_brand = rec.x_studio_field_U36cw
