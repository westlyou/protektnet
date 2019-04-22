# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models


class ProjectTaskPOWizard(models.TransientModel):
    _name = 'project.task.po.wizard'
    _description = "Create RFQ from Project Taks"

    partner_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        domain=[('supplier', '=', True)],
        required=True,)
    line_ids = fields.One2many(
        'project.task.po.wizard.line', 'wiz_id', string='Lines',)

    @api.model
    def _prepare_item(self, line):
        return {
            'product_id': line.product_id.id,
            'qty': line.qty,
            'uom_id': line.uom_id.id,
            'unit_price': line.unit_price,
            'subtotal': line.subtotal,
            'name': line.product_id.display_name,
            'analytic_tag_ids': [
                (6, 0, line.task_id.analytic_tag_id.ids)],
            'analytic_account_id': (
                line.task_id.project_id.analytic_account_id.id),
        }

    @api.model
    def default_get(self, res_fields):
        res = super().default_get(res_fields)
        tasks = self.env['project.task'].browse(
            self._context.get('active_ids'))
        lines = []
        for line in tasks.mapped('total_resource_ids'):
            lines.append([0, 0, self._prepare_item(line)])
        res.update({
            'line_ids': lines,
        })
        return res

    @api.model
    def _prepare_po_line(self, line):
        return {
            'product_id': line.product_id.id,
            'name': line.name,
            'product_qty': line.qty,
            'price_unit': line.subtotal,
            'product_uom': line.uom_id.id,
            'date_planned': fields.Datetime.now(),
            'account_analytic_id': line.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)]
        }

    @api.model
    def _prepare_purchase_order(self, partner, lines):
        return {
            'partner_id': partner.id,
            'order_line': lines,
            'date_planned': fields.Datetime.now(),
            'task_ids': [(6, 0, self._context.get('active_ids'))],
        }

    @api.multi
    def create_purchase_order(self):
        for rec in self:
            lines = []
            for line in rec.line_ids:
                lines.append((0, 0, self._prepare_po_line(line)))
            res = self.env['purchase.order'].create(
                self._prepare_purchase_order(rec.partner_id, lines))
            return {
                'name': _('Purchase Order'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'purchase.order',
                'res_id': res.id,
                'target': 'current',
                'type': 'ir.actions.act_window',
            }


class ProjectTaskPOWizardLine(models.TransientModel):
    _name = 'project.task.po.wizard.line'
    _description = "Project Task PO Wizard Lines"

    wiz_id = fields.Many2one('project.task.po.wizard',)
    name = fields.Char(required=True,)
    product_id = fields.Many2one('product.product', required=True,)
    qty = fields.Float(required=True,)
    uom_id = fields.Many2one('product.uom', required=True,)
    unit_price = fields.Float(required=True,)
    subtotal = fields.Float(compute='_compute_subtotal')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', required=True,)
    analytic_account_id = fields.Many2one(
        'account.analytic.account', required=True,)

    @api.depends('unit_price', 'qty')
    @api.multi
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.unit_price
