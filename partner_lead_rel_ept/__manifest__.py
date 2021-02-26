{
    'name': 'Partner Lead Relationship',
    'version': '1.0',
    'summary': 'Partner and their relationships with leads.',
    'description': 'Detailed partner and their leads relationships content.',
    'author': 'Raumil D',
    'depends': ['base','crm','sale'],
    'data': ['Security/ir.model.access.csv',
             'Views/partner_lead.xml','Views/sale_orders.xml'],
    'installable': True,
    'auto_install': False
}
