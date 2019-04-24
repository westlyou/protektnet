# Copyright 2019, Jarsa Sistemas, S.A. de C.V.
# Copyright 2019 Grupo Censere.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Projects from crm/Sale order',
    'summary': 'Module to create projects from crm or sale order',
    'version': '11.0.1.0.0',
    'category': 'Sale',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project_template',
        'crm',
    ],
    'data': [
        'views/crm_lead_view.xml',
    ],
}
