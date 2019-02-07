# -*- coding: utf-8 -*-
# © <2019> <Grupo Censere>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_brand = fields.Selection(
        string="Brand", readonly=True, related="product_id.product_brand",
        store=True)
