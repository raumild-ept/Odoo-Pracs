from odoo import fields, models, api


class ProductStockUpdate(models.TransientModel):
    _name = 'stock.product.update.ept'
    _description = 'Product Stock Update'

    location_id = fields.Many2one(comodel_name='stock.location.ept',
                                  string="Location ID",
                                  domain=[('location_type', '=', 'Internal')])
    current_stock = fields.Float(digits=(6, 2), string="Current Stock ")
    counted_qty = fields.Float(digits=(6, 2), string="Counted Stock ")
    difference_qty = fields.Float(compute='_compute_diff', digits=(6, 2), string="Difference ")

    @api.onchange('location_id')
    def _check_current_stock(self):
        if self.location_id:
            product = self.env['product.ept.sales'].with_context(loc=self.location_id.id).browse(
                self.env.context.get('active_id'))
            self.current_stock = product.product_stock
        elif not self.location_id:
            self.current_stock = 0

    def _compute_diff(self):
        self.difference_qty = self.counted_qty - self.current_stock

    def submit_product_update(self):
        product = self.env['product.ept.sales'].with_context(loc=self.location_id.id).browse(
            self.env.context.get('active_id'))
        stock_inventory = self.env['stock.inventory.ept'].create({
            'name': f'{product.name}_inventory',
            'location_id': self.location_id.id})
        self.env['stock.inventory.line.ept'].create({
            'product_id': product.id,
            'inventory_id': stock_inventory.id,
            'available_qty': self.current_stock,
            'counted_product_qty': self.counted_qty
        })
        stock_inventory.validate_inventory()
