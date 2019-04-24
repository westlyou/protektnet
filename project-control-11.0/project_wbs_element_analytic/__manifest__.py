# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# Copyright 2019 Grupo Censere.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Project WBS Element Analytic',
    'summary': 'This application creates analytic tags when a WBS'
    'element or a task is created.',
    'version': '11.0.1.0.0',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'category': 'Project',
    'license': 'AGPL-3',
    'depends': [
        'project_wbs_element',
        'project_analytic',
    ],
    'data': [
        'views/project_wbs_element_view.xml',
    ],
}
