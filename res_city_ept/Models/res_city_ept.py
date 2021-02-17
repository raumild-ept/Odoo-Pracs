from odoo import api, fields, models, SUPERUSER_ID, _

class ResCityEpt(models.Model):
    _name = "res.city.ept"
    _description = "This is Res_City_Ept Module."
    _rec_name = "city"
    city = fields.Char(string = "City" ,help = "Enter Your City")
    state = fields.Char(string = "State" ,help = "Enter Your State")
    active = fields.Boolean(string = "Active" ,help = "Is it Active", default = True)