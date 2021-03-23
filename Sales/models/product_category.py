from odoo import fields, models


class ProductCat(models.Model):
    _name = "product.category.ept"
    _description = "Product Category."

    name = fields.Char(string="Name ", help="Name of Category.")
    parent_id = fields.Many2one(comodel_name='product.category.ept',
                                string="Parent Category",
                                help="Name of Parent Category.")
