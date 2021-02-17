from odoo import api, fields, models, SUPERUSER_ID, _

class ResPartnerEpt(models.Model):
    _name = "res.partner.sales.ept"
    _description = "Res Partner Sales."

    name = fields.Char(string = 'Name', required = True, help = 'Name Of Partner')
    mobile = fields.Char(string="Mobile",help="Please Enter Mobile Number")
    description = fields.Text(string = 'Description',help="Description")
    gender = fields.Selection([('Male','Male'),('Female','Female'),('Transgender','Transgender')],string = 'Gender',store = True)
    street1 = fields.Char(string = "Address Street 1" , help = "Please enter Address street 1")
    street2 = fields.Char(string="Address Street 2", help="Please enter Address street 2")
    city =fields.Many2one(comodel_name ='res.city1.ept',string = "City" , help = "Please enter City")
    state1 = fields.Many2one(comodel_name ='res.state1.ept',string="State", help="Please enter State")
    country1 = fields.Many2one(comodel_name ='res.country1.ept',string="Country", help="Please enter Country")
    email = fields.Char(string="Email", help="Please enter Email")
    zipcode = fields.Char(string = "Zipcode",help = "Please enter Zipcode")
    phone = fields.Char(string="Phone",help="Please Enter Phone Number")
    image100 = fields.Image("Photo",max_height=100,max_width=100)
    website =fields.Char(string="Website",help="Enter Website")
    active = fields.Boolean(string = "Active",help="Is Active",default = True)
    parent_id = fields.Many2one(comodel_name ='res.partner.sales.ept',string="Parent")
    child_ids = fields.One2many(comodel_name ='res.partner.sales.ept',inverse_name='parent_id',string="Child Ids")
    address_type = fields.Selection([('Invoice','Invoice'),('Shipping','Shipping'),('Contact','Contact')],string = 'Address Type')

    def name_get(self):
        result_list = list()
        for record in self:
            name_data = (record.id, str(record.name) +"-"+ str(record.country1.country))
            result_list.append(name_data)
        return result_list



