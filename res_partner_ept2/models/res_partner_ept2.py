from odoo import api, fields, models, SUPERUSER_ID, _


class ResPartnerEpt2(models.Model):
    _name = "res.partner.ept2"
    _description = "This is my Second."

    name = fields.Char(string='Name', required=True, help='Enter Your Name')
    birthdate = fields.Date(string='Birthdate', required=True, help='Enter Birthdate')
    age = fields.Integer(string='Age', help="Enter Age")
    description = fields.Text(string='Description', help="Enter your description.")
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')], string='Gender',
                              store=True, help="Enter Gender")
    details = fields.Html(string='Details')
    is_spectacles = fields.Boolean(string='Spectacles',
                                   help='is True if you have spectacles')
    street1 = fields.Char(string="Address Street 1", help="Please enter Address street 1")
    street2 = fields.Char(string="Address Street 2", help="Please enter Address street 2")
    city = fields.Char(string="City", help="Please enter City")
    state = fields.Char(string="State", help="Please enter State")
    country = fields.Char(string="Country", help="Please enter Country")
    zipcode = fields.Char(string="Zipcode", help="Please enter Zipcode")
    weight = fields.Integer(string="Weight", help="Please enter your weight.")
