from odoo import fields, models


class Move(models.Model):
    _name = 'stock.move.ept'
    _description = 'Stock Move'

    name = fields.Char(string="Description", help="Store Product Name")
    product_id = fields.Many2one(comodel_name='product.ept.sales',
                                 string='Product_ID',
                                 help='Select Product ID')
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string='UOM_ID',
                             help='Select UOM ID')
    source_location_id = fields.Many2one(comodel_name='stock.location.ept',
                                         string='Source Location',
                                         help='Source Location')
    destination_location_id = fields.Many2one(comodel_name='stock.location.ept',
                                              string='Destination Location',
                                              help='Destination Location')
    qty_to_deliver = fields.Float(string="Quantity To Deliver", digits=(6, 2))
    qty_delivered = fields.Float(string="Quantity Delivered", digits=(6, 2))
    state = fields.Selection(selection=[('Draft', 'Draft'),
                                        ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')],
                             string="State ")
    sale_line_id = fields.Many2one(comodel_name='sale.order.line.ept',
                                   string="Order Line")
    stock_inventory_id = fields.Many2one(comodel_name='stock.inventory.ept',
                                         string='Stock Inventory')
    picking_id = fields.Many2one(comodel_name='stock.picking.ept',
                                 string='Picking ID')
