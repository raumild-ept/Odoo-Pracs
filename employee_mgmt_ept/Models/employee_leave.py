from odoo import fields, models

class EmpLeaves(models.Model):
    _name = "employee.leave.ept"
    _description = "Employee Leave Model"

    employee_id = fields.Many2one(comodel_name ='res.employee.mgmt.ept',string = "Employee")
    dept_id = fields.Many2one(comodel_name ='employee.department.ept',string = 'Department')
    department = fields.Many2one(related = "employee_id.dept_id" , string = "Department")
    start_date = fields.Date(string = "Start Date",required = True)
    end_date = fields.Date(string = "End Date",required = True)
    status = fields.Selection(selection = [('Draft','Draft'),
                                           ('Approved','Approved'),
                                           ('Refused','Refused'),
                                           ('Cancelled','Cancelled')],
                              string = "Status",help="Leave Status")
    leave_desc = fields.Char(string = "Leave Description",help = "Description of Leave.")