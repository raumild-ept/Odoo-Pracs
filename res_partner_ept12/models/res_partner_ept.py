from odoo import api, fields, models, SUPERUSER_ID, _

class ResPartnersEpt(models.Model):
    _name = "res.partner.ept"
    _description = "res.partner.ept"

    name = fields.Char(string='Name', required=True,help='Please enter partner name')
    street1 = fields.Char(string='Street1', required=True,help='Please enter partner street1')
    street2 = fields.Char(string='Street2', required=True,help='Please enter partner street2')
    city = fields.Char(string='City', required=True,help='Please enter partner city')
    state = fields.Char(string='State', required=True,help='Please enter partner state')
    zip_code = fields.Char(string='Zip_code', required=True,help='Please enter partner zip_code')
    country = fields.Char(string='Country', required=True,help='Please enter partner country')
    birthdate = fields.Date(string='Birthdate')
    age = fields.Integer(string='Age')
    weight = fields.Float('Weight', digits=0)
    description = fields.Text('Description')
    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
        ], string='Gender', store=True,)
    details = fields.Html(string='Details')
    is_spectacles = fields.Boolean(string='Is spectacles',help="Please check if partner has spectacles")

