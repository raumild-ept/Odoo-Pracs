from odoo import api, models, fields, SUPERUSER_ID, _

class ResCountryEpt(models.Model):
    _name = "res.country.ept"
    _description = "description of res.country.ept"

    _rec_name = "country"
    country = fields.Char(string="Country Name", required=True, help="Please enter country name.")
    c_code = fields.Char(string="Country Code", required=True, help="Please enter country code")
    active_is = fields.Selection([('Active', 'Active'), ('Inactive', 'Inactive')], string="Active/Inactive",
                              required=True, default="Active")

