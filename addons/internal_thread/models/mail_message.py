# -*- coding: utf-8 -*-

from odoo import api, models, SUPERUSER_ID


class mail_message(models.Model):
    _inherit = 'mail.message'

    @api.multi
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._uid != SUPERUSER_ID:
            group_ids = self.env.user.groups_id
            group_user_id = self.env.ref('base.group_user')
            mt_internal_mes = self.env.ref('internal_thread.mt_internal_mes').id

            if group_user_id.id not in [group_id for group_id in group_ids.ids]:
                args = [('subtype_id', '!=', mt_internal_mes)] + list(args)

        return super(mail_message, self)._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
