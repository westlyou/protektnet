# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _inherit = 'mail.thread'

    code = fields.Char()
    name = fields.Char(required=True)
    description = fields.Text()
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
    )
    parent_id = fields.Many2one(
        'project.wbs_element',
        string='Parent WBS Element',
    )
    child_ids = fields.One2many(
        comodel_name='project.wbs_element',
        inverse_name='parent_id',
        string='Child WBS Elements',
    )
    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='wbs_element_id',
        string='Tasks',
    )
    nbr_tasks = fields.Integer(
        string='Number of Tasks',
        compute='_compute_count_tasks',
    )
    nbr_childs = fields.Integer(
        string='Number of Child WBS Elements',
        compute='_compute_count_childs',
    )
    nbr_docs = fields.Integer(
        string='Number of Documents',
        compute='_compute_count_attached_docs',
    )
    color = fields.Integer(
        string='Color Index',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        compute='_compute_partner_id',
        store=True,)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The code of the WBS Element must be unique.')]

    @api.depends('project_id')
    def _compute_partner_id(self):
        for rec in self:
            if rec.project_id:
                rec.partner_id = rec.project_id.partner_id.id

    @api.depends('task_ids')
    def _compute_count_tasks(self):
        for record in self:
            record.nbr_tasks = len(record.task_ids)

    @api.depends('child_ids')
    def _compute_count_childs(self):
        for record in self:
            record.nbr_childs = len(record.child_ids)

    @api.multi
    def _compute_count_attached_docs(self):
        attachment = self.env['ir.attachment']
        task = self.env['project.task']
        for record in self:
            project_attachments = attachment.search(
                [('res_model', '=', 'project.wbs_element'),
                 ('res_id', '=', record.id)])
            tasks = task.search([('wbs_element_id', '=', record.id)])
            task_attachments = attachment.search(
                [('res_model', '=', 'project.task'),
                 ('res_id', 'in', tasks.ids)])
            record.nbr_docs = \
                (len(project_attachments) or 0) + (len(task_attachments) or 0)

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id:
            self.project_id = self.parent_id.project_id

    @api.multi
    @api.constrains('child_ids', 'task_ids')
    def _check_tasks_assigned(self):
        for record in self:
            if record.child_ids and record.task_ids:
                raise ValidationError(
                    _('A WBS Element that is parent of others cannot have '
                      'tasks assigned.'))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for record in self.child_ids:
            record.project_id = record.project_id

    @api.multi
    def attachment_tree_view(self):
        tasks = self.env['project.task'].search([
            ('project_id', 'in', self.ids)])
        domain = [
            '|',
            '&', ('res_model', '=', 'project.wbs_element'), (
                'res_id', 'in',
                self.ids),
            '&', ('res_model', '=', 'project.task'), ('res_id', 'in',
                                                      tasks.ids)
        ]
        res_id = self.ids and self.ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (
                self._name, res_id)
        }

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.child_ids:
                raise ValidationError(
                    _("Oops! This WBS element actually have "
                      "Childs elements. \nYou must delete his childs "
                      "before continue."))
            elif rec.task_ids:
                raise ValidationError(
                    _("Oops! This WBS element actually have "
                      "tasks. \n You must delete his tasks "
                      "before continue."))
            return super().unlink()

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            if rec.code:
                name = '[%s] %s' % (rec.code, rec.name)
            res.append((rec.id, name))
        return res
