from odoo import api, SUPERUSER_ID, fields, models, _

class EmployeeEpt(models.Model):
    _name = "employee.ept"
    _description = "This is employee ept."
    _rec_name = "emp_name"

    emp_name = fields.Char(string="Name",required= True,help = "Name of Employee")
    emp_dept = fields.Char(string="Department",  help="Department of Employee")
    job_position = fields.Char(string="Job Position", help="Job Position of Employee")
    salary = fields.Float(string="Salary",digits = (6,2), help="Salary of Employee")
    join_date = fields.Date(string="Joining Date", help="Joining Date of Employee")
    gender = fields.Selection(selection = [('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')], string='Gender',
                              store=True, help="Gender of Employee")
    job_type = fields.Selection(selection = [('Permanent','Permanent'),('Ad_Hoc','Ad_Hoc')], string = "job_type",help = "Job Type of an employee")