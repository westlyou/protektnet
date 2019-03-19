# -*- coding: utf-8 -*-
##########################################################################
#
#  Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#  See LICENSE file for full copyright and licensing details.
#  License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models


class MagentoCustomers(models.Model):
    _name = "magento.customers"
    _order = 'id desc'
    _rec_name = "cus_name"
    _description = "Magento Customers"

    cus_name = fields.Many2one('res.partner', string='Customer Name')
    oe_customer_id = fields.Integer(string='Odoo Customer Id')
    mag_customer_id = fields.Char(string='Magento Customer Id', size=50)
    instance_id = fields.Many2one(
        'magento.configure', string='Magento Instance')
    mag_address_id = fields.Char(string='Magento Address Id', size=50)
    need_sync = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No')
    ], default="No", string='Update Required')
    created_by = fields.Char(string='Created By', default="odoo", size=64)
    create_date = fields.Datetime(string='Created Date')
    write_date = fields.Datetime(string='Updated Date')

    @api.model
    def create(self, vals):
        ctx = dict(self._context or {})
        if ctx.get('instance_id'):
            vals['instance_id'] = ctx.get('instance_id')
            cust_mage = self.search([
                ('cus_name', '=', vals['cus_name']),
                ('oe_customer_id', '=', vals['oe_customer_id']),
                ('mag_customer_id', '=', vals['mag_customer_id']),
                ('mag_address_id', '=', vals['mag_address_id']),
                ('created_by', '=', vals['created_by']),
                ('instance_id', '=', vals['instance_id']),
            ])
            if cust_mage:
                return cust_mage
        return super(MagentoCustomers, self).create(vals)
