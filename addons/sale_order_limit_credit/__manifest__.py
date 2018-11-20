# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Sale Order Limit Credit",
    'summary': "",
    'author': 'Sarai Osorio',
    'website': 'http://grupocensere.com/',
    'category': 'Sales',
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'depends': [
        'sale'
    ],
    'data': [
        'views/res_config_settings_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ]
}
