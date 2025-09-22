{
    'name': 'ToDo Custom',
    'version': '1.0',
    'summary': 'Simple ToDo Task Manager',
    'category': 'Productivity',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_task_views.xml',
        'wizards/mark_done_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
}
