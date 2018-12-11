# -*- coding: utf-8 -*-
# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Payment Schedule Date',
    'summary': 'This module helps control the payment date.',
    'version': '11.0.1.0.0',
    'category': 'Account',
    'website': 'https://www.grupocensere.com/',
    'author': 'Grupo Censere (<https://www.grupocensere.com>)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'account',
        'l10n_mx_edi',
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ]
}
