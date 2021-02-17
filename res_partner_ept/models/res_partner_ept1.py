from odoo import api, fields, models, SUPERUSER_ID, _

class ResPartnerEpt(models.Model):
    _name = "res.partner.ept1"
    _description = "This is my first."

    name = fields.Char(string = 'Name', required = True, help = 'Helpppppp')
    birthdate = fields.Date(string = 'Birthdate', required = True, help = 'Help bdate' )
    age = fields.Integer(string = 'Age')
    description = fields.Text(string = 'Description')
    gender = fields.Selection([('Male','Male'),('Female','Female'),('Transgender','Transgender')],string = 'Gender',store = True)
    details = fields.Html(string='Details')
    is_spectacles = fields.Boolean(string='Spectacles', default=True,
                                   help='is True if you have spectacles')
    street1 = fields.Char(string = "Address Street 1" , help = "Please enter Address street 1")
    street2 = fields.Char(string="Address Street 2", help="Please enter Address street 2")
    city =fields.Char(string = "City" , help = "Please enter City")
    state = fields.Char(string="State", help="Please enter State")
    country = fields.Char(string="Country", help="Please enter Country")
    zipcode = fields.Char(string = "Zipcode",help = "Please enter Zipcode")
    weight = fields.Integer(string = "Weight" , help = "Please enter your weight.")