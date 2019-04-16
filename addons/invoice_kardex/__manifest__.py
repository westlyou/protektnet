# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Invoice Kardex',
    'summary': 'View and create reports',
    'category': 'Account',
    'description': """
Inovice Reports
==================
    """,
    'depends': [
        'stock',
        'account',
        'account_reports',
        'customs_grupo_censere',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/invoice_kardex_data.xml',
        'views/report_invoice.xml',
        'views/search_template_view.xml'
    ],
    'qweb': [
        'static/src/xml/invoice_kardex_template.xml',
    ],
    'auto_install': True,
    'installable': True,
    'license': 'OEEL-1',
}
