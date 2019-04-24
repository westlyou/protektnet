# Copyright 2019 Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Demos',
    'summary': 'Module for create stock of demos',
    'version': '11.0.1.0.0',
    'category': 'stock',
    'website': 'https://odoo-community.org/',
    'author': 'Grupo Censere',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'product',
        'stock',
        'customs_grupo_censere',
    ],
    'data': [
        'views/product_product_view.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
        'views/stock_location_view.xml',
        'views/stock_return_picking_view.xml',
    ],
}
