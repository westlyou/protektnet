# Copyright 2018 Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Sale Order Customs",
    'summary': "",
    'website': 'https://www.grupocensere.com/',
    'author': 'Grupo Censere (<https://www.grupocensere.com>)',
    'category': 'Sales',
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'depends': [
        'sale',
        'sale_stock',
        'purchase_order_customs',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
    ]
}
