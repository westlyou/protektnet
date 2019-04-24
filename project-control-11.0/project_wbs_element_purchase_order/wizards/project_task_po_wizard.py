# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ProjectTaskPOWizard(models.TransientModel):
    _inherit = 'project.task.po.wizard'

    @api.model
    def _get_analytic_wbs_tags(self, line):
        def recursive_tags(wbs, tag_ids):
            tag_ids.append(wbs.analytic_tag_id.id)
            if wbs.parent_id:
                tag_ids = recursive_tags(wbs.parent_id, tag_ids)
            return tag_ids
        tag_ids = []
        return recursive_tags(line.wbs_element_id, tag_ids)

    @api.model
    def _prepare_item(self, line):
        """Method to append the WBS analytic tags to the wizard line"""
        res = super()._prepare_item(line)
        analytic_tag_ids = (
            res['analytic_tag_ids'][0][2] + self._get_analytic_wbs_tags(
                line.task_id))
        res['analytic_tag_ids'] = [(6, 0, analytic_tag_ids)]
        return res

    @api.model
    def _prepare_po_line(self, line):
        """Method to append the WBS analytic tags to the purchase order line"""
        res = super()._prepare_po_line(line)
        analytic_tag_ids = (
            res['analytic_tag_ids'][0][2] + line.analytic_tag_ids.ids)
        res['analytic_tag_ids'] = [(6, 0, analytic_tag_ids)]
        return res
