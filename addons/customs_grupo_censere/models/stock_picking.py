# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import datetime
import ast


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        parameters = self.env['ir.config_parameter']
        users = ast.literal_eval(parameters.get_param('activity_users'))
        sale_order = self.env['sale.order'].search([('name', '=', res.origin)])
        acti_types = sale_order.order_line.mapped(
            'product_id').mapped('uom_id').mapped('name')
        any_day = fields.Date.from_string(fields.Date.today())
        date = self.last_day_of_month(any_day)
        if res.picking_type_code == 'outgoing':
            for act_type in acti_types:
                res.activity_ids.create({
                    'activity_type_id': 4,
                    'summary': 'Salida de Almacén',
                    'date_deadline': date,
                    'user_id': self.env['res.users'].search([
                        ('name', '=', users[act_type])]).id,
                    'res_model_id': self.env['ir.model'].search([
                        ('model', '=', 'stock.picking')], limit=1).id,
                    'res_id': res.id,
                })
        return res

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def button_validate(self):
        if self.env.user.has_group(
                'customs_grupo_censere.group_block_picking_product'):
            for rec in self:
                value = sum(rec.move_lines.filtered(
                    lambda x: x.product_id.categ_id.id == 4
                ).mapped('quantity_done'))
                if value != 0:
                    raise ValidationError(
                        _('Warning!! You can not give physical products out of'
                            ' stock. Communicate with your administrator.'))
        return super(StockPicking, self).button_validate()
