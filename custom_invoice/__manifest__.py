{
    'name': 'Customer Invoice Custom Report',
    'version': '1.0',
    'depends': ['account','base'],
    'category': 'Accounting',
    'summary': 'Custom QWeb report for customer invoices',
    'description': 'Simple customer invoice report with company logo, customer info, lines, totals, amount in words',
    'data': [
        'report/customer_invoice_report_template.xml',
    ],
    'installable': True,
    'application': False,
}
