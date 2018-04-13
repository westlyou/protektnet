# -*- coding: utf-8 -*-
# Author: Red Lab.
# Copyright: Red Lab.

{
    'name': 'Convert Sale Order to Purchase Order/RFQ',
    'images': ['images/main_screenshot.png'],
    'version': '2.1.2',
    'category': 'Sales',
    'summary': 'Converting Sale Order to Purchase Order/RFQ with single button click,'
               ' transfer all important and compatible data. Configurable in settings.',
    'author': 'Red Lab',
    'website': 'lab.stone.red@gmail.com',
    'price': 34.00,
    'currency': 'EUR',
    'depends': [
        'so_po_field',
        'po_so_field',
    ],
    'data': [
        'views/sale_views.xml',
        'views/sale_config_views.xml',
    ],
}
