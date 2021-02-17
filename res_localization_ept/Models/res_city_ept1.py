from odoo import api, fields, models, SUPERUSER_ID, _

class ResCityEpt(models.Model):
    _name = "res.city1.ept"
    _description = "This is Res_City_Ept Module."

    _rec_name = "city"
    city = fields.Char(string = "City" ,help = "Enter Your City")
    state_id = fields.Many2one(comodel_name ='res.state1.ept',string = "State Name")
