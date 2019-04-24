# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision


class TaskResource(models.Model):
    _name = "task.resource"
    _description = "Task Unit Resource(s)"

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
        digits=decimal_precision.get_precision('Product Unit of Measure'),
    )
    description = fields.Char()
    resource_type_id = fields.Many2one(
        comodel_name='resource.type',
        string='Resource type',
    )
    unit_price = fields.Float()

    @api.onchange('product_id')
    def product_id_change(self):
        description = ''
        uom_id = False
        product = self.product_id
        if product:
            description = product.name_get()[0][1]
            uom_id = product.uom_id.id
        if product.description_purchase:
            description += ' - %s' % product.description_purchase
        self.update({
            'description': description,
            'uom_id': uom_id,
            'unit_price': self.product_id.list_price,
        })
