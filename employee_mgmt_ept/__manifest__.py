{
    'name':'employee_mgmt_ept',
    'author':'Raumil D',
    'description':'This is Emp Management Module',
    'summary': 'Employee Management',
    'depends': ['base'],
    'data':['Security/security.xml','Security/ir.model.access.csv',
            'Views/department.xml',
            'Views/menu.xml',
            'Views/leaves.xml',
            'Views/employee.xml',
            'Views/shift.xml'],
    'demo':[],
    'installable':True
}