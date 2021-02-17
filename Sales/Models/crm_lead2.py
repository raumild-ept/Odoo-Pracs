from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import date


class CrmLeadEpt(models.Model):
    _name = "crm.lead.ept2"
    _description = "This is crm_lead_ept _description."
    _rec_name = "cust_name"

    cust_name = fields.Char(string="Customer Name", required=True, help="Name of Customer")
    cust_email = fields.Char(string="Email", help="Email of Customer")
    cust_phone = fields.Char(string="Phone", help="Phone No of Customer")
    partner_id = fields.Many2one(comodel_name='res.partner.sales.ept',string='Partner',domain= "[('parent_id','=',False)]")
    revenue = fields.Float(string="Revenue", help="Revenue of Customer")

    sales_person_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user.id,
                                   string="Salesperson", help="Name Of SalesPerson", required=True)
    sales_team = fields.Char(string="Sales Team", help="Name Of Sales Team")
    campaign = fields.Char(string="Campaign", help="Name of Campaign")
    state = fields.Selection(selection=[('New', 'New'),
                                        ('Qualified', 'Qualified'),
                                        ('Proposition', 'Proposition'),
                                        ('Won', 'Won'),
                                        ('Lost', 'Lost')], help="Select State", string="State")
    channel = fields.Selection(selection=[('Facebook', 'Facebook'),
                                          ('WhatsApp', 'WhatsApp'),
                                          ('Email', 'Email'),
                                          ('Newspaper', 'Newspaper'),
                                          ('Television', 'Television'),
                                          ('Phone Call', 'Phone Call'),
                                          ('SMS', 'SMS'),
                                          ('Google Ads', 'Google Ads')], help="Select Channel", string="Channel")
    follow_up_date = fields.Date(string="Follow Up Date", required=True, help="Next follow up date.")
    won_date = fields.Date(string="Won Date", domain="[('state','=','Won')]", help="Won date.")
    lost_reason = fields.Text(string="Lost Reason", domain="[('state','=','Lost')]", help="Enter Reason Why Lost")
    order_ids = fields.One2many(comodel_name="sale.orders.ept",inverse_name="lead_id",string= "Orders",readonly = True)
    lead_line_ids = fields.One2many(comodel_name='crm.lead.line.ept', inverse_name='lead_id', string="Lead lines")

    def set_to_won(self):
        self.state = 'Won'
        self.won_date = date.today()

    def create_sale_order(self):
        if self.partner_id:
            address_data = self.env['res.partner.sales.ept']
            i = 0
            j = 0
            invoicer = 0
            ship = 0
            for child in self.partner_id.child_ids:
                if child.address_type == 'Invoice' and i == 0:
                    invoicer = child
                    i += 1
                elif child.address_type == 'Shipping' and j == 0:
                    ship = child
                    j += 1
                elif i == 1 and j == 1:
                    break
            if invoicer != 0:
                invoicer = invoicer.id
            if ship != 0:
                ship = ship.id

            order = self.env['sale.orders.ept'].create({'customer_id': self.partner_id.id,
                                                'sale_order_date': date.today(),
                                                'salesperson_id': self.sales_person_id.id,
                                                'state': 'Draft',
                                                'invoice_customer_id': invoicer,
                                                'shipping_customer_id': ship,
                                                'lead_id': self.id
                                                })

            if self.lead_line_ids:
                for lead_line in self.lead_line_ids:
                    self.env['sale.order.line.ept'].create({'order_no_id':order.id,
                                                            'product_name_id':lead_line.product_id.id,
                                                            'quantity':lead_line.sell_qty,
                                                            'uom_id':lead_line.uom_id.id})


    def create_customer(self):
        partner_data = self.env['res.partner.sales.ept']
        partner_data.create({'name': self.cust_name,
                             'email':self.cust_email,
                             'mobile':self.cust_phone,
                             })
        temp = partner_data.search([('name','=',self.cust_name),('mobile','=',self.cust_phone)])
        self.partner_id = temp.id

    def set_to_lost(self):
        self.state = 'Lost'
        self.lost_reason = "Unknown"