# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Project Task Resource',
    'summary': 'Manage Resources on project tasks',
    'version': '11.0.1.0.0',
    'category': 'Project',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'project_analytic',
        'product',
    ],
    'data': [
        'data/resource_type_data.xml',
        'security/ir.model.access.csv',
        'views/project_project_view.xml',
        'views/project_task_view.xml',
        'views/resource_type_view.xml',
        'views/total_task_resource_view.xml',
    ],
}
