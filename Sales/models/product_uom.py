from odoo import fields, models


class ProductUom(models.Model):
    _name = "product.uom.ept"
    _description = "Product UOM Model."

    name = fields.Char(string="Name ", help="Name Of UoM")
    uom_category_id = fields.Many2one(comodel_name='product.uom.category.ept',
                                      string="UoM Category",
                                      help="Category of UoM")
