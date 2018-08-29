# -*- coding: utf-8 -*-
{
    'name': 'Private Thread',
    'version': '1.1',
    'category': 'Discuss',
    'summary': 'A tool for private communication with colleagues',
    'description': '''
Private Thread and Discussions
==============================
The app is a tool to communicate with colleagues without interrupting followers.
Odoo default functionality assumes each time you send a message all subscribers (including partners) are notified.
As an alternative you may log an internal note without notifications.
This approach hardly suits in a case you would like to communicate something important only to your colleague.
This app let avoid excess emails but simultaneously notify required partners.
* Notifications are not sent to the followers disregarding their subscription
* Messages are visible for ones who may see the parent object except portal users
* In order to send such a message it is enough to flag a check box on email composer form
* You may use an app also to check system messages such as sending a quotation to a customers
* The app equally works for all objects (sales orders, invoices, issues, etc.)
    ''',
    'price': '49.00',
    'currency': 'EUR',
    'auto_install': False,
    'application': True,
    'author': 'IT Libertas',
    'website': 'https://odootools.com',
    'depends': [
        'super_mail',
    ],
    'data': [
        'views/thread.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
    ],
    'js': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'license': 'Other proprietary',
    'images': ['static/description/main.png'],
    'update_xml': [],
    'installable': True,
    'private_category': False,
    'external_dependencies': {
    },
}
