from odoo import api, fields, models, SUPERUSER_ID, _


class ProductEpt(models.Model):
    _name = "product.ept.rdb"
    _description = "Product module for products."

    name = fields.Char(string="Enter Product Name",  help="Enter Product Name ")
    sku = fields.Integer(string="SKU", help="Enter Stock Keeping Unit")
    barcode = fields.Char(string="Barcode", help="Enter Barcode ")
    salable = fields.Boolean(string="Salable", help="Can This Product Be Sold")
    product_type = fields.Selection([('storable', 'Storable'), ('consumable', 'Consumable'), ('service', 'Service')],
                                    string="Type", help="Enter Type Of Product")
    sale_price = fields.Float(digits=(6, 2), string="Sale Price", help="Enter Sale Price")

    cost_price = fields.Float(digits=(6, 2), string="Cost Price", help="Enter Cost Price")
    active = fields.Boolean(string="Active", default= True,help="Select if Active")
    warehouse = fields.Char(string="Warehouse", help="Enter Warehouse ")
    image_256 = fields.Image("Image", max_width=128, max_height=128,
                             )
    states = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    website_desc = fields.Html(string="Website Description", help="Enter Website Description. ")
    notes = fields.Text(string="Internal Note", help="Enter Internal notes.")
