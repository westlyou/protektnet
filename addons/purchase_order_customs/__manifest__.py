# -*- coding: utf-8 -*-
# Copyright 2018, Grupo Censere (<http://grupocensere.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Price',
    'summary': 'Price from supplier',
    'version': '11.0.1.0.0',
    'category': 'Purchase',
    'website': 'http://grupocensere.com/',
    'author': '<Grupo Censere (<http://grupocensere.com/>)',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'purchase'
    ],
    'data': [
        'views/purchase_order_view.xml',
    ],
}
