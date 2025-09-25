{
    'name': 'Mobile Model Management',
    'version': '1.0',
    'summary': 'Manage mobile phone models',
    'category': 'Productivity',
    'author': 'Your Name',
    'depends': ['base', 'approvals'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'views/mobile_view.xml',
        'views/mobile_menu.xml',
        'wizards/mobile_consumer_bill_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}
