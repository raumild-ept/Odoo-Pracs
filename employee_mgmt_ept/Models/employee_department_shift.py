from odoo import models, fields

class EmpDeptShift(models.Model):
    _name = "employee.shift.ept"
    _description= "Employee Department Shift"
    _rec_name = "shift"

    shift = fields.Selection(
        selection=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('Night', 'Night')],
        string="Select Shift")
