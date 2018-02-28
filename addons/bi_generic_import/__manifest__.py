# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo all import for Sales, Purchase, Invoice, Inventory, Customer/Supplier Payment, Bank Statement, Journal Entry, Picking, Product, Customer.',
    'version': '11.0.0.0',
    'sequence': 4,
    'summary': 'Easy to import all odoo data i.e Invoice, Sale, Inventory, Purchase,Payment, Picking, Product and Customer.',
    'price': 129,
    'currency': 'EUR',
    'category' : 'Extra Tools',
    'description': """

	BrowseInfo developed a new odoo/OpenERP module apps 
	This module use for following easy import.
	Import Stock from CSV and Excel file.
    Import Stock inventory from CSV and Excel file.
	Import inventory adjustment, import stock balance
	Import opening stock balance from CSV and Excel file.
	Import Sale order, Import sales order, Import Purchase order, Import purchases.
	Import sale order line, import purchase order line, Import data, Import files, Import data from third party software
	Import invoice from CSV, Import Bulk invoices easily.Import warehouse data,Import warehouse stock.Import product stock.
	Invoice import from CSV, Invoice line import from CSV, Sale import, purchase import
	Inventory import from CSV, stock import from CSV, Inventory adjustment import, Opening stock import. 
	Import product from CSV, Import customer from CSV, Product Import,Customer import, Odoo CSV bridge,Import CSV brige on Odoo.Import csv data on odoo.All import, easy import, Import odoo data, Import CSV files, Import excel files 
	Import tools Odoo, Import reports, import accounting data, import sales data, import purchase data, import data in odoo, import record, Import inventory.import data on odoo,Import data from Excel, Import data from CSV.Odoo Import Data

	-Import product from CSV and Excel file.
	-Import product from Excel and CSV file.
	-Import variant from CSV and Excel file.
	-Import variant from Excel and CSV file.
	-Import product variant from CSV and Excel file.
	-Import product variant from Excel and CSV file.

	-Import item from CSV and Excel file.
	-Import item from Excel and CSV file.

	-Import partner from CSV and Excel file.
	-Import vendor from csv and excel file
	-Import partner from Excel and CSV file.
	-Import contact from CSV and Excel file.
	-Import contact from Excel and CSV file.
	-Import Customer from CSV and Excel file.
	-Import customer from Excel and CSV file.
	-Import Supplier from CSV and Excel file.
	-Import supplier from Excel and CSV file.

	item import from csv, product import from csv, catelog import from csv, contact import from csv, partner import from csv, customer import from csv, supplier import from csv,variant import from csv, product variant import from csv, vendor import from csv

	item import from excel, product import from excel, catelog import from excel, contact import from excel, partner import from excel, customer import from excel, supplier import from excel,variant import from excel, product variant import from excel, vendor import from excel

	item import csv, product import csv, catelog import csv, contact import csv, partner import csv, customer import csv, supplier import csv,variant import csv, product variant import csv, vendor import csv

	item import excel, product import excel, catelog import excel, contact import excel, partner import excel, customer import excel, supplier import excel,variant import excel, product variant import excel, vendor import excel
    """,
    'author': 'BrowseInfo',
    'website': '',
    'live_test_url':'https://www.youtube.com/watch?v=bG7ImzFkSfo',
    'depends': ['base', 'sale_management', 'account', 'purchase', 'stock','product_expiry'],
    'data': [
             "views/account_invoice.xml",
             "views/purchase_invoice.xml",
             "views/sale.xml",
             "views/stock_view.xml",
             "views/product_view.xml",
             "views/partner.xml",
             "views/picking_view.xml",
             "views/customer_payment.xml",
             "views/import_order_lines_view.xml",
             "views/import_po_lines_view.xml",
             "views/import_invoice_lines_view.xml",
             "views/bank_statement.xml",
             "views/import_image_view.xml",
             "views/account_move.xml",
             "views/supp_info.xml",
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images':['static/description/Banner.png'],



}
