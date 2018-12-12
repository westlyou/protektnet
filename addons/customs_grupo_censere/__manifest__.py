# Copyright 2018 Grupo Censere.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Customs from Grupo Censere',
    'summary': 'This module is for create customs in the workflow of company',
    'version': '11.0.1.0.0',
    'category': 'Customs',
    'website': 'https://www.grupocensere.com/',
    'author': 'Grupo Censere (<https://www.grupocensere.com>)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'l10n_mx_edi',
        'sale_stock',
        'sale',
        'stock',
        'bi_manual_currency_exchange_rate',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
}
