# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import Warning
import binascii
import tempfile
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class import_invoice_wizard(models.TransientModel):

	_name='import.invoice.wizard'

	invoice_file = fields.Binary(string="Select File")

	@api.multi
	def import_inv(self):
		fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
		fp.write(binascii.a2b_base64(self.invoice_file))
		fp.seek(0)
		values = {}
		workbook = xlrd.open_workbook(fp.name)
		sheet = workbook.sheet_by_index(0)
		for row_no in range(sheet.nrows):
			val = {}
			if row_no <= 0:
				fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
			else:
				line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
				values.update({
								'product':line[0],
								'quantity':line[1],
								'uom':line[2],
								'description':line[3],
								'price':line[4],
								'tax':line[5],
							})
				res = self.create_inv_line(values)
		return res

	@api.multi
	def create_inv_line(self,values):
		account_inv_brw=self.env['account.invoice'].browse(self._context.get('active_id'))
		product=values.get('product')
		uom=values.get('uom')
		product_obj_search=self.env['product.product'].search([('name','=',product)])
		uom_obj_search=self.env['product.uom'].search([('name','=',uom)])
		
		if not uom_obj_search:
			raise Warning(_('UOM "%s" is Not Available') % uom)

		if product_obj_search:
			product_id=product_obj_search
		else:
			product_id=self.env['product.product'].create({'name':product,'lst_price':values.get('price')})

		if account_inv_brw.type == "out_invoice" and account_inv_brw.state == 'draft':
			tax_id_lst=[]
			if values.get('tax'):
			    if ';' in  values.get('tax'):
			        tax_names = values.get('tax').split(';')
			        for name in tax_names:
			            tax= self.env['account.tax'].search([('name', '=', name),('type_tax_use','=','sale')])
			            if not tax:
			                raise Warning(_('"%s" Tax not in your system') % name)
			            tax_id_lst.append(tax.id)
			    elif ',' in  values.get('tax'):
			        tax_names = values.get('tax').split(',')
			        for name in tax_names:
			            tax= self.env['account.tax'].search([('name', '=', name),('type_tax_use','=','sale')])
			            if not tax:
			                raise Warning(_('"%s" Tax not in your system') % name)
			            tax_id_lst.append(tax.id)
			    else:
			        tax_names = values.get('tax').split(',')
			        tax= self.env['account.tax'].search([('name', '=', tax_names),('type_tax_use','=','sale')])
			        if not tax:
			            raise Warning(_('"%s" Tax not in your system') % tax_names)
			        tax_id_lst.append(tax.id)
				
					

			cust_account_id = product_id.property_account_income_id.id
			if cust_account_id:
				account_id = cust_account_id
			else:
				account_id = product_id.categ_id.property_account_income_categ_id.id	

			inv_lines=self.env['account.invoice.line'].create({
												'account_id':account_id,
												'invoice_id':account_inv_brw.id,
												'product_id':product_id.id,
												'name':product,
												'quantity':values.get('quantity'),
												'uom_id':uom_obj_search.id,
												'price_unit':values.get('price')
												})
			if tax_id_lst:
				inv_lines.write({'invoice_line_tax_ids':([(6,0,tax_id_lst)])})
			return True

		elif account_inv_brw.type =="in_invoice" and account_inv_brw.state == 'draft':
			tax_id_lst=[]
			if values.get('tax'):
				name_tax = values.get('tax').split(';')
				for each in name_tax:
					tax_id=self.env['account.tax'].search([('name','=',each),
														('type_tax_use','=','purchase')])
					if not tax_id:
						raise Warning(_('Tax "%s" is Not Available') % each)
					tax_id_lst.append(tax_id.id)

			vendor_account_id = product_id.property_account_expense_id.id
			if vendor_account_id:
				account_id = vendor_account_id
			else:
				account_id = product_id.categ_id.property_account_expense_categ_id.id


			inv_lines=self.env['account.invoice.line'].create({
												'account_id':account_id,
												'invoice_id':account_inv_brw.id,
												'product_id':product_id.id,
												'name':product,
												'quantity':values.get('quantity'),
												'uom_id':uom_obj_search.id,
												'price_unit':values.get('price')
												})
			if tax_id_lst:
				inv_lines.write({'invoice_line_tax_ids':([(6,0,[tax_id_lst])])})
			return True
			
		elif account_inv_brw.state != 'draft':
			raise UserError(_('We cannot import data in validated or confirmed Invoice.'))
		

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
