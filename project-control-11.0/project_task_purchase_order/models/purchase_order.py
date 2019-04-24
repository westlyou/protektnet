# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    task_ids = fields.Many2many(
        'project.task',
        string="Project Task(s)",)
