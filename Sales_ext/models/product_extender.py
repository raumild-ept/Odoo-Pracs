from odoo import fields, models, api


class ProductExtender(models.Model):
    _inherit = 'product.template'
    _description = 'Product Extended'

    deposit_product_id = fields.Many2one(comodel_name='product.product',string="Deposit Product",help="Add deposit product.")
    deposit_product_qty = fields.Integer(string="Deposit Product Quantity")