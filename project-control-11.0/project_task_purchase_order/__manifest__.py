# Copyright 2018 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Project Task to Purchase Order',
    'summary': 'Make RFQ from Project Tasks',
    'version': '11.0.1.0.0',
    'category': 'Project',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
        'project_task_resource',
    ],
    'data': [
        'wizards/project_task_po_wizard.xml',
        'views/project_task.xml',
    ],
}
