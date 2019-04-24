# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision
from odoo.tools.translate import _


class ProjectTask(models.Model):
    _inherit = "project.task"

    resource_ids = fields.One2many(
        comodel_name='task.resource',
        inverse_name='task_id',
        string='Unit Resource(s)',
    )
    total_resource_ids = fields.One2many(
        comodel_name='task.resource.total',
        inverse_name='task_id',
        string='Total Resource(s)',)
    qty = fields.Float(
        string='Quantity',
        default=1,
        digits=decimal_precision.get_precision('Product Unit of Measure'),
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    unit_price = fields.Float()
    subtotal = fields.Float(
        compute='_compute_value_subtotal',
        store=True,
    )

    @api.multi
    @api.depends('qty', 'unit_price')
    def _compute_value_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price

    @api.multi
    def write(self, values):
        res = super(ProjectTask, self).write(values)
        for rec in self:
            if (rec.total_resource_ids and
                    fields.Datetime.now() ==
                    rec.total_resource_ids.mapped('create_date')[0]):
                return res
            rec.total_resource_ids.unlink()
            for resource in rec.resource_ids:
                rec.total_resource_ids = (0, 0, {
                    'task_id': rec.id,
                    'project_id': rec.project_id.id,
                    'product_id': resource.product_id.id,
                    'description': resource.description,
                    'resource_type_id': resource.resource_type_id.id,
                    'uom_id': resource.uom_id.id,
                    'qty': rec.qty * resource.qty,
                    'unit_price': resource.unit_price,
                    'real_qty': rec.qty * resource.qty,
                    'subtotal': (
                        rec.qty * resource.qty * (
                            resource.unit_price))
                })
        return res

    @api.multi
    def action_task_resource_total(self):
        self.ensure_one()
        return {
            'name': _('Task Resource(s)'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'task.resource.total',
            'domain': [('task_id', '=', self.id)],
            'type': 'ir.actions.act_window',
        }
