# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision


class TaskResourceTotal(models.Model):
    _name = "task.resource.total"
    _description = "Task Resource(s)"

    name = fields.Char()
    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        related='task_id.project_id',
    )
    resource_type_id = fields.Many2one(
        comodel_name='resource.type',
        string='Resources Type',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product')
    description = fields.Char()
    qty = fields.Float(
        string="Quantity",
        digits=decimal_precision.get_precision('Product Unit of Measure'),
    )
    real_qty = fields.Float(
        string="Quantity Real",
        digits=decimal_precision.get_precision('Product Unit of Measure'),
    )
    unit_price = fields.Float()
    subtotal = fields.Float()
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )

    @api.onchange('product_id')
    def onchange_product(self):
        self.description = self.product_id.description
        self.uom_id = self.product_id.uom_id
        self.account_id = self.task_id.analytic_account_id
