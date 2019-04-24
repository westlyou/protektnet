# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    @api.model_cr
    def init(self):
        """Remove the sql constrains that validate the code as unique """
        cr = self._cr
        cr.execute('''
            ALTER TABLE public.project_wbs_element
            DROP CONSTRAINT project_wbs_element_code_uniq''')

    @api.model
    def _get_wbs_code(self, rec):
        prefix = ''
        sufix = ''
        # Search the WBS siblings
        wbs_siblings = self.search(
            [('id', '!=', rec.id),
             ('project_id', '=', rec.project_id.id),
             ('parent_id', '=', rec.parent_id.id)], order='code')

        # If not siblings the sufix will be 1 by default
        if not wbs_siblings:
            sufix = '1'
            # If the wbs has a wbs parent the code must have
            # the parent's code and a dot as prefix
            if rec.parent_id:
                prefix = rec.parent_id.code + '.'
            return prefix + sufix

        # If the wbs has a wbs parent the code must have
        # the parent's code and a dot as prefix
        if rec.parent_id:
            prefix = rec.parent_id.code + '.'
        # Get the last number of the code to sum 1
        last_wbs_code = wbs_siblings[-1].code[-1]
        sufix = str(int(last_wbs_code) + 1)
        return prefix + sufix

    @api.model
    def create(self, values):
        rec = super().create(values)
        rec.code = self._get_wbs_code(rec)
        return rec

    @api.multi
    def write(self, values):
        to_write = self
        for rec in self:
            if ('name' in values or 'parent_id' in values and
                    'code' not in values):
                values['code'] = rec._get_wbs_code(rec)
                super(ProjectWbsElement, rec).write(values)
                to_write -= rec
        return super(ProjectWbsElement, to_write).write(values)

    @api.multi
    def _reorder_wbs_codes(self):
        for rec in self:
            # if the record is the first we do not do anything
            if not self.ids.index(rec.id):
                old_wbs_code = rec.code
                continue
            # We save the code before update to save after the wbs update
            code_before_update = rec.code
            # Update the current wbs code
            rec.code = old_wbs_code
            # Save the code before update to use it on the next loop
            old_wbs_code = code_before_update

    @api.multi
    def unlink(self):
        to_unlink = self
        for rec in self:
            # Get the WBS element of the current level
            wbs_siblings = self.search(
                [('project_id', '=', rec.project_id.id),
                 ('parent_id', '=', rec.parent_id.id)], order='code')
            # We get the list of ids to search the current element index
            # in order to get the right element to reorganize the codes
            wbs_siblings_ids = wbs_siblings.ids
            wbs_index = wbs_siblings_ids.index(rec.id)
            # We browse right WBS elements
            right_wbs_elements = self.browse(wbs_siblings_ids[wbs_index:])
            right_wbs_elements._reorder_wbs_codes()
            to_unlink -= rec
            super(ProjectWbsElement, rec).unlink()
        return super(ProjectWbsElement, to_unlink).unlink()
