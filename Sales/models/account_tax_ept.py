from odoo import fields, models


class AccountTax(models.Model):
    _name = 'account.tax.ept'
    _description = 'Account Tax'

    name = fields.Char()
    tax_use = fields.Selection(selection=[('None', 'None'),
                                          ('Sales', 'Sales'),
                                          ('Purchase', 'Purchase')],
                               string="Tax Use ")
    tax_value = fields.Float(string="Percentage ", help='Enter Tax Value')
    tax_amount_type = fields.Selection(selection=[('Percentage', 'Percentage'),
                                                  ('Fixed', 'Fixed')],
                                       string="Tax Type ", default='Percentage')
