from odoo import api,fields, models, SUPERUSER_ID, _

class AddressBook(models.Model):
    _name = "res.partner.ept3"
    _description = "This is Address Book or Contacts Created 3rd time"

    name = fields.Char(string = "Name", required = True,help = "Enter your Name")
    street1= fields.Char(string="Street 1", help="Enter Address Street 1")
    street2= fields.Char(string="Street 2", help="Enter Address Street 2")
    city = fields.Char(string = "City", help = "Enter the City")
    state = fields.Char(string = "State", help = "Enter Your State" )
    country = fields.Char(string = 'Country', help = "Enter Country")
    zipcode = fields.Char(String = 'zipcode',help = "Enter Zipcode")
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')], string='Gender',
                              store=True, help="Enter Gender")
    birthdate = fields.Date(string = "Birthdate",help = "Enter BirthDate")
    age= fields.Integer(string = "Age", help= "Enter Age")
    weight = fields.Integer(string = "Weight", help = "Enter Age")
    has_spectacles = fields.Boolean (string ="Has Specs", help ="Select if you have specs." )
    details = fields.Html(string = "Details")
    desc = fields.Text(string = "Description", help ="Enter Description.")