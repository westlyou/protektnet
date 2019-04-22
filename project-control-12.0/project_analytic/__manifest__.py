# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project Analytic',
    'summary': 'Analytic Account on Project and Analytic Tags on Tasks',
    'version': '11.0.1.0.0',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'category': 'Project',
    'license': 'AGPL-3',
    'depends': ['project', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_account_view.xml',
        'views/project_task_view.xml',
    ],
}
