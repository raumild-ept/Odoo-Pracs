from odoo import api, fields, models, SUPERUSER_ID, _

class ResStateEpt(models.Model):
    _name = "res.state.ept"
    _description = "This is res_state_ept"

    _rec_name = "state_name"
    state_name = fields.Char(string = "State", required = True,copy = False)
    state_code = fields.Char(string = "State Code", required = True)
    country = fields.Char(string = "Country Name", required = True)
    active = fields.Boolean(string = ("Active"))
