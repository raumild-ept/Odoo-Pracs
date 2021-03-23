{
    'name': 'Sales Extended',
    'version': '1.0',
    'summary': 'none',
    'description': 'none',
    'author': 'Emipro Technologies (P) Ltd.',
    'depends': ['delivery', 'Sales', 'sale_crm', ],
    'data': ['security/ir.model.access.csv','security/security.xml',
             'views/cron.xml',
             'views/setting.xml',
             'views/extended.xml',
             'views/product.xml',
             'views/sale_line.xml',
             'views/sale_order_line.xml',
             'wizard/sales_data.xml'
             ],
    'installable': True,
    'auto_install': False
}
