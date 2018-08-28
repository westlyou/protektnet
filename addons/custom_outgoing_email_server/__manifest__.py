{
    'name': 'Custom Outgoing Email Server',
    'images': ['images/main_screenshot.jpg'],
    'summary': """Allow to pick the Outgoing Server when composing email""",
    'version': '11.0.1.0.0',
    'author': 'BUSO Co. Ltd',
    'license': 'AGPL-3',
    'website': 'https://www.busovn.com',
    'category': 'web',
    'depends': ['mail'],
    'data': [
        'wizard/mail_compose_message_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'web_preload': True,
}
