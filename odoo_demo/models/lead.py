from odoo import fields, models, api


class Lead(models.Model):
    _name = 'odoo.demo.lead'
    _description = 'Odoo Demo'

    name = fields.Char(string='Lead')
    partner_id = fields.Many2one(string='Organisation/Contact',comodel_name='res.partner')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    expected_revenue = fields.Float(string = 'Expected Revenue')
    priority = fields.Integer(string="Priority")
    color = fields.Integer(string='Color')

