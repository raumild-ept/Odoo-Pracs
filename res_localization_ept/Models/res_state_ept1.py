from odoo import api, fields, models, SUPERUSER_ID, _

class ResStateEpt(models.Model):
    _name = "res.state1.ept"
    _description = "This is res_state_ept.)"

    _rec_name = "state"
    state = fields.Char(string = "State", required = True)
    s_code = fields.Char(string = "State Code", required = True)
    country_id = fields.Many2one(comodel_name ='res.country1.ept',string = "Country Name")
    city_ids = fields.One2many(comodel_name ='res.city1.ept',inverse_name='state_id',string = "City Names")

    _sql_constraints = [('s_code', 'unique(s_code)', 'The code of state must be unique.')]

