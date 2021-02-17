from odoo import fields, models, api


class InventoryLine(models.Model):
    _name = 'stock.inventory.line.ept'
    _description = 'Inventory Line'
    _rec_name = 'product_id'


    product_id = fields.Many2one(comodel_name='product.ept.sales',string='Product ID')
    inventory_id = fields.Many2one(comodel_name='stock.inventory.ept',string='Inventory ID',readonly=True)
    available_qty = fields.Float(digits=(6,2),string='Available Quantity',readonly=True)
    counted_product_qty = fields.Float(digits=(6,2),string='Counted Product Quantity')
    difference = fields.Float(compute = '_compute_difference',string = 'Difference',readonly = True)


    def _compute_difference(self):
        for record in self:
            record.difference = record.counted_product_qty - record.available_qty

