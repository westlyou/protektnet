# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'send_email_inventory',
    'summary': 'Module for send email of inventory ',
    'version': '11.0.1.0.0',
    'category': 'stock',
    'website': 'https://odoo-community.org/',
    'author': 'Grupo Censere',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock'
    ],
    'data': [
        'views/ir_cron_inventory.xml',
    ],
}
