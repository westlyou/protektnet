from odoo import _, api, fields, models
from email.utils import formataddr

class XMailThreadIgnoreCatchAllSystemParameter(models.AbstractModel):

	_inherit = 'mail.thread'

	@api.model
	def message_get_reply_to(self, res_ids, default=None):
		""" Returns the preferred reply-to email address that is basically the
		alias of the document, if it exists. Override this method to implement
		a custom behavior about reply-to for generated emails. """
		model_name = self.env.context.get('thread_model') or self._name
		alias_domain = self.env['ir.config_parameter'].sudo().get_param("mail.catchall.domain")
		res = dict.fromkeys(res_ids, False)

		# alias domain: check for aliases and catchall
		aliases = {}
		doc_names = {}
		if alias_domain:
			if model_name and model_name != 'mail.thread' and res_ids:
				mail_aliases = self.env['mail.alias'].sudo().search([
					('alias_parent_model_id.model', '=', model_name),
					('alias_parent_thread_id', 'in', res_ids),
					('alias_name', '!=', False)])
				# take only first found alias for each thread_id, to match
				# order (1 found -> limit=1 for each res_id)
				for alias in mail_aliases:
					if alias.alias_parent_thread_id not in aliases:
						aliases[alias.alias_parent_thread_id] = '%s@%s' % (alias.alias_name, alias_domain)
				doc_names.update(
					dict((ng_res[0], ng_res[1])
						 for ng_res in self.env[model_name].sudo().browse(aliases).name_get()))
			# left ids: use catchall
			left_ids = set(res_ids).difference(set(aliases))
			#Ignore catchall
			"""if left_ids:
				catchall_alias = self.env['ir.config_parameter'].sudo().get_param("mail.catchall.alias")
				if catchall_alias:
					aliases.update(dict((res_id, '%s@%s' % (catchall_alias, alias_domain)) for res_id in left_ids))"""
			# compute name of reply-to
			user_name = self.env.user.name
			for res_id in aliases:
				email_name = '%s%s' % (user_name, doc_names.get(res_id) and (' ' + doc_names[res_id]) or '')
				email_addr = aliases[res_id]
				res[res_id] = formataddr((email_name, email_addr))
		left_ids = set(res_ids).difference(set(aliases))
		if left_ids:
			res.update(dict((res_id, default) for res_id in res_ids))
		return res
