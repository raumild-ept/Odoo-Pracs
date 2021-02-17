from odoo import fields, models, api


class Location(models.Model):
    _name = 'stock.location.ept'
    _description = 'Stock Location'

    name = fields.Char(string = "Name",help="Name Of Location")
    parent_id=fields.Many2one(comodel_name='stock.location.ept',
                              string='Parent Location',help="Name of Parent Location.")
    location_type = fields.Selection(selection = [('Vendor','Vendor'),
                                                  ('Customer','Customer'),
                                                  ('Internal','Internal'),
                                                  ('Inventory Loss','Inventory Loss'),
                                                  ('Production','Production'),
                                                  ('Transit','Transit'),
                                                  ('View','View')],string='Location Type',
                                    help="Select type of Location.")
    is_scrap_location = fields.Boolean(string="Is Scrap Location",help="Is scrap location?")