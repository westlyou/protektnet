# -*- coding: utf-8 -*-
# Copyright 2018, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Censere Customs',
    'summary': 'Module summary',
    'version': '11.0.1.0.0',
    'category': 'Uncategorized',
    'website': 'http://grupocensere.com',
    'author': '<Grupo Censere>',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'account',
        'l10n_mx_edi',
        'purchase',
        'stock',
    ],
    'data': [
        'views/account_account_view.xml',
        'views/account_invoice_view.xml',
        'views/account_payment_view.xml',
        'views/product_supplierinfo_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/res_user_view.xml',
        'views/stock_move_view.xml',
        'views/stock_picking_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ]
}
