# Copyright 2019 Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Report Sales',
    'summary': 'This modulo view report for sales',
    'version': '11.0.1.0.0',
    'category': 'sale',
    'website': 'https://odoo-community.org/',
    'author': 'Grupo Censere',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
    ],
    'data': [
        'wizards/report_sale_wizard_view.xml',
        'report/report_sale.xml',
    ],
}
