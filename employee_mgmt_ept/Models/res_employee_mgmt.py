from odoo import fields, models

class EmployeeMgmt(models.Model):
    _name="res.employee.mgmt.ept"
    _description="Employee Management"

    name = fields.Char(string="Name", required = True, help= "Name of The Employee")
    dept_id = fields.Many2one(comodel_name ='employee.department.ept', string="Name", required=True, help="Name of The Employee")
    shift_id = fields.Many2one(comodel_name ='employee.shift.ept',string="Shift",help="Shift of Employee")
    emp_position = fields.Char(string="Job Position",  help= "Employee Job Position.")
    salary = fields.Float(string="Salary",help="Salary Of Employee.")
    hire_date=fields.Date(string="Hire Date",help="Hiring Date")
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')], string='Gender',
                              store=True, help="Enter Gender")
    job_type = fields.Selection(selection = [('Permanent','Permanent'),('Ad_Hoc','Ad_Hoc')], string = "Job Type",help = "Job Type of an employee")
    is_manager = fields.Boolean (string ="Is Manager?", help ="Select if employee is Manager." )
    manager_id = fields.Many2one(comodel_name ='res.employee.mgmt.ept',string = "Manager",help="Name of the Manager.")
    related_user_id = fields.Many2one(comodel_name ='res.users',string="Related User",help="Name of related User")
    employees_under_manager_ids = fields.One2many(comodel_name='res.employee.mgmt.ept',
                                                  inverse_name='manager_id',
                                                  string="Employees Under Manager")
