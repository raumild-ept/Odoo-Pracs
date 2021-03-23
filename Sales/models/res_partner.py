from datetime import date
from odoo import api, fields, models


class ResPartnerEpt(models.Model):
    _name = "res.partner.sales.ept"
    _description = "Res Partner Sales."

    name = fields.Char(string='Name ', required=True,
                       help='Name Of Partner')
    mobile = fields.Char(string="Mobile ", help="Please Enter Mobile Number")
    description = fields.Text(string='Description ', help="Description")
    bdate = fields.Date(string='Birth Date ')
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female'),
                               ('Transgender', 'Transgender')],
                              string='Gender ',
                              store=True)
    street1 = fields.Char(string="Address Street 1 ",
                          help="Please enter Address street 1")
    street2 = fields.Char(string="Address Street 2 ",
                          help="Please enter Address street 2")
    city = fields.Many2one(comodel_name='res.city1.ept',
                           string="City ", help="Please enter City")
    state1 = fields.Many2one(comodel_name='res.state1.ept',
                             string="State ", help="Please enter State")
    country1 = fields.Many2one(comodel_name='res.country1.ept',
                               string="Country ", help="Please enter Country")
    email = fields.Char(string="Email ", help="Please enter Email")
    zipcode = fields.Char(string="Zipcode ", help="Please enter Zipcode")
    phone = fields.Char(string="Phone ", help="Please Enter Phone Number")
    image100 = fields.Image("Photo ", max_height=100, max_width=100)
    website = fields.Char(string="Website ", help="Enter Website")
    active = fields.Boolean(string="Active ", help="Is Active", default=True)
    parent_id = fields.Many2one(comodel_name='res.partner.sales.ept', string="Parent ")
    child_ids = fields.One2many(comodel_name='res.partner.sales.ept',
                                inverse_name='parent_id', string="Child Ids ")
    address_type = fields.Selection([('Invoice', 'Invoice'),
                                     ('Shipping', 'Shipping'),
                                     ('Contact', 'Contact')],
                                    string='Address Type ')
    age_calculate = fields.Integer(compute="_compute_age",
                                   search='_search_age', string='Age')
    age_calculate_readonly = fields.Integer(string='Age R')

    @api.onchange('bdate')
    def _compute_age(self):
        for record in self:
            if record.bdate:
                today = date.today()
                record.age_calculate = today.year - \
                                       record.bdate.year - \
                                       ((today.month, today.day)
                                        < (record.bdate.month, record.bdate.day))
            else:
                record.age_calculate = 0

    def _search_age(self, opr, val):
        sql = f"select id from res_partner_sales_ept " \
              f"where bdate is not null " \
              f"and date_part('year',age(now(),bdate))" \
              f" {opr} {val};"
        self._cr.execute(sql)
        domain = self._cr.fetchall()
        return [('id', 'in', domain)]

    @api.onchange('bdate')
    def _com_age2(self):
        for record in self:
            if record.bdate:
                if date.today().month < record.bdate.month:
                    record.age_calculate_readonly = date.today().year - \
                                                    record.bdate.year - 1
                else:
                    record.age_calculate_readonly = date.today().year \
                                                    - record.bdate.year

    def name_get(self):
        result_list = list()
        for record in self:
            name_data = (record.id, str(record.name) +
                         "-" +
                         str(record.country1.country))
            result_list.append(name_data)
        return result_list
