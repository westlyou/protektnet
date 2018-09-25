# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    "name" : "Currency Exchange Rate on Invoice/Payment/Sale/Purchase",
    "version" : "11.0.0.1",
    "depends" : ['base','account_invoicing','account','purchase','sale_management'],
    "author": "BrowseInfo",
    "summary": "This module helps to apply manual currency rate on invoice, payment, sales and purchase order ",
    "description": """
    Odoo/OpenERP module for manul currency rate converter
    Currency Exchange Rate on Invoice/Payment/Sale/Purchase, manual multi currency process on invoice, multi currency payment
    Currency Exchange Rate on Payment/Sale/Purchase
    Manual Currency Exchange Rate on invoice payment
    Manual Currency Rate on invoice payment
    Currency Exchange Rate on Sales order
    Currency Exchange Rate on Sale order
    Currency Exchange Rate on Purchase Order
    Apply Manual Currency Exchange Rate on Invoice/Payment/Sale/Purchase
    Apply Manual Currency Exchange Rate on Payment
    Apply Manual Currency Exchange Rate on Sale Order
    Apply Manual Currency Exchange Rate on Purchase Order

    Apply Manual Currency Rate on Invoice/Payment/Sale/Purchase
    Apply Manual Currency Rate on Payment
    Apply Manual Currency Rate on Sale Order
    Apply Manual Currency Rate on Purchase Order
    multi-currency process on invoice, multi-currency payment
    currency converter on Odoo
    invoice currency rate
    Manual Exchange rate of Currency apply
    manual currency rate on invoice
    currency rate apply manually

    """,
    "price": 89,
    "currency": "EUR",
    'category': 'Accounting',
    "website" : "www.browseinfo.in",
    "data" :[
             "views/customer_invoice.xml",
             "views/account_payment_view.xml",
             "views/purchase_view.xml",
             "views/sale_view.xml",
    ],
    'qweb':[
    ],
    "auto_install": False,
    "installable": True,
	"images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
