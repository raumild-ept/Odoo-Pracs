from odoo import fields, models


class ProductUomCat(models.Model):
    _name = "product.uom.category.ept"
    _description = "Product UoM Category."

    name = fields.Char(string="Name ",
                       help="Category Name")
