from odoo import api,fields,models,SUPERUSER_ID, _
from datetime import date

class CrmLeadEpt(models.Model):
    _name="crm.lead.ept"
    _description="This is crm_lead_ept _description."
    _rec_name = "cust_name"
    cust_name = fields.Char(string = "Customer Name", required = True, help="Name of Customer")
    cust_email = fields.Char(string="Email", required=True, help="Email of Customer")
    cust_phone = fields.Char(string="Phone", required=True, help="Phone No of Customer")
    revenue = fields.Float(string="Revenue", help="Revenue of Customer")
    sales_person = fields.Char(string="Salesperson", help="Name Of SalesPerson",required = True)
    sales_team = fields.Char(string="Sales Team", help="Name Of Sales Team")
    campaign = fields.Char(string="Campaign", help="Name of Campaign")
    state = fields.Selection(selection = [('New','New'),
                                            ('Qualified','Qualified'),
                                            ('Proposition','Proposition'),
                                            ('Won','Won'),
                                            ('Lost','Lost')],required = True, help = "Select State",string="State")
    channel = fields.Selection(selection = [('Facebook','Facebook'),
                                            ('WhatsApp','WhatsApp'),
                                            ('Email','Email'),
                                            ('Newspaper','Newspaper'),
                                            ('Television','Television'),
                                            ('Phone Call','Phone Call'),
                                            ('SMS','SMS'),
                                            ('Google Ads','Google Ads')],required = True, help = "Select Channel",string="Channel")
    follow_up_date = fields.Date(string = "Follow Up Date",required = True,help = "Next follow up date.")
    won_date = fields.Date(string = "Won Date",domain = "[('state','=','Won')]",help = "Won date.")
    lost_reason = fields.Text(string  = "Lost Reason",domain = "[('state','=','Lost')]",help = "Enter Reason Why Lost")




