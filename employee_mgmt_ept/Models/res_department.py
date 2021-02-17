from odoo import models, fields

class EmployeeEpt(models.Model):
    _name = "employee.department.ept"
    _description = "employee department management"

    name = fields.Char(string="Department Name", help="Name of the department.")
    employee_ids = fields.One2many(comodel_name ='res.employee.mgmt.ept',inverse_name='dept_id',string="Employee Names")
    dept_manager = fields.Many2one(comodel_name ='res.users',string = "Department Manager")