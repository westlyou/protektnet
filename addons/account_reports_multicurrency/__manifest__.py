# Copyright 2019 Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'account_reports_multicurrency',
    'summary': 'inherit of account_reports',
    'version': '11.0.1.0.0',
    'category': 'account',
    'website': 'https://odoo-community.org/',
    'author': 'Grupo Censere',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'account_reports',
    ],
    'data': [
        'views/search_template_view.xml',
    ],
}
