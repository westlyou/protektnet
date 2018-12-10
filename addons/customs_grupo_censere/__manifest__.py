# Copyright 2018 Grupo Censere.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Customs from Grupo Censere',
    'summary': 'This module is for create customs in the workflow of company',
    'version': '11.0.1.0.0',
    'category': 'Customs',
    'website': 'https://odoo-community.org/',
    'author': 'Grupo Censere',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'l10n_mx_edi',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
}
