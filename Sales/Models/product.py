from odoo import api, fields, models, SUPERUSER_ID, _


class ProductEpt(models.Model):
    _name = "product.ept.sales"
    _description = "Product model."

    name = fields.Char(string="Enter Product Name", required=True, help="Enter Product Name ")
    sku = fields.Integer(string="SKU", help="Enter Stock Keeping Unit")
    barcode = fields.Char(string="Barcode", help="Enter Barcode ")
    salable = fields.Boolean(string="Salable", help="Can This Product Be Sold")
    product_type = fields.Selection([('Storable', 'Storable'), ('Consumable', 'Consumable'), ('Service', 'Service')],
                                    string="Type", help="Enter Type Of Product")
    sale_price = fields.Float(digits=(6, 2), string="Sale Price", default='5.00', help="Enter Sale Price")
    cost_price = fields.Float(digits=(6, 2), string="Cost Price", default='5.00', help="Enter Cost Price")
    length = fields.Float(digits=(6, 2), string="Length", help="Enter Length")
    width = fields.Float(digits=(6, 2), string=" Width", help="Enter Width")
    weight = fields.Float(digits=(6, 2), string="Weight", help="Enter Weight")
    volume = fields.Float(digits=(6, 2), string="Volume", help="Enter Volume")
    product_cat_id = fields.Many2one(comodel_name='product.category.ept', string="Product Category",
                                     help="Product Category")
    product_uom_id = fields.Many2one(comodel_name='product.uom.ept', string="UOM", help="Product UoM")
    product_stock = fields.Float(digits=(6, 2), strong='Product Stock', readonly=True, store=False,
                                 compute='_compute_stock')
    tax_ids = fields.Many2many(comodel_name="account.tax.ept",string = "Taxes",help="Taxes")

    def _compute_stock(self):
        warehouses = self.env['stock.warehouse.ept'].search([])
        stock_loc = self.env.context.get('loc')
        stock = 0
        for product in self:
            stock = 0
            if stock_loc:
                stock += self.count_quantity(stock_loc,product)
                product.product_stock = stock
            else:
                for warehouse in warehouses:
                    stock += self.count_quantity(warehouse.stock_location_id.id,product)
                    product.product_stock = stock

    def count_quantity(self,stock_loc,product):
        stock = 0
        to_plus = self.env['stock.move.ept'].search(
            [('product_id', '=', product.id), ('destination_location_id', '=', stock_loc), ('state', '=', 'Done')])
        to_minus = self.env['stock.move.ept'].search(
            [('product_id', '=', product.id), ('source_location_id', '=', stock_loc), ('state', '=', 'Done')])
        for record in to_plus:
            stock += record.qty_delivered
        for record in to_minus:
            stock -= record.qty_delivered
        return stock


    def update_stock_wizard(self):
        view_id = self.env.ref('Sales.view_form_stock_update').id
        return {
                'type': 'ir.actions.act_window',
                'name': _('Update Stock'),
                'res_model': 'stock.product.update.ept',
                'target': 'new',
                'view_mode': 'form',
                'views': [[view_id, 'form']],
                }

