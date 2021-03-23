from odoo import fields, models


class Warehouse(models.Model):
    _name = 'stock.warehouse.ept'
    _description = 'Stock Warehouse'

    name = fields.Char(string="Name ", help="Name Of Inventory")
    short_code = fields.Char(string="Short Code ", help="Short Code")
    address = fields.Many2one(comodel_name='res.partner.sales.ept',
                              string="Address ", help="Address")
    stock_location_id = fields.Many2one(comodel_name='stock.location.ept',
                                        string='Stock Location ',
                                        domain=[('location_type', '=', 'Internal')],
                                        help="Stock Location")
