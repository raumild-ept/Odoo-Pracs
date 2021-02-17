# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.s

{
    'name':'Res_partner_Ept',
    'version':'1.1',
    'category': 'Sales',
    'summary': 'Demo partner odoo',
    'description': """
This demo are made for learning purpose
    """,
    'depends': ['sales_team'],
    'data': ['views/res_partner_ept.xml',
             'security/ir.model.access.csv',
             ],
    'demo': ['Data/Demo_data.xml'],
    'installable' : True,
    'auto_install' : False
}




