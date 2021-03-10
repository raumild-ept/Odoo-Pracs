{
    'name': 'Sales Extended',
    'version': '1.0',
    'summary': 'none',
    'description': 'none',
    'author': 'Raumil D',
    'depends': ['delivery','Sales','sale_crm',],
    'data': ['security/ir.model.access.csv',
             'views/cron.xml',
             'views/report_template.xml',
             'views/extended.xml',
             'views/product.xml',
             'views/sale_line.xml'],
    'installable': True,
    'auto_install': False
}
