from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line"
    _rec_name = "order_no_id"

    order_no_id = fields.Many2one(comodel_name='sale.orders.ept', string="Order No")
    product_name_id = fields.Many2one(comodel_name='product.ept.sales', string="Product")
    uom_id = fields.Many2one(related='product_name_id.product_uom_id', string="UoM")
    quantity = fields.Float(string="Quantity", digits=(6, 2))
    unit_price = fields.Float(string="Unit Price", digits=(6, 2))
    state = fields.Selection(selection=[('Draft', 'Draft'),
                                        ('Confirmed', 'Confirmed'),
                                        ('Cancelled', 'Cancelled')], string="State",default='Draft')
    subtotal_nodb = fields.Float(compute='_compute_subtotal',
                                 string="Subtotal NODB",
                                 readonly=True,
                                 store=False)
    subtotal_onchange = fields.Float(string="SubTotal ONC", store=True)
    subtotal_ondepends = fields.Float(compute='_compute_sub_ondepends', string="SubTotal OND", store=True)
    picking_id = fields.Many2one(comodel_name='stock.picking.ept', string='Picking ID')
    stock_move_ids = fields.One2many(comodel_name='stock.move.ept', inverse_name='sale_line_id', string="Stock Moves")
    delivered_qty = fields.Float(string="Delivered QTY", digits=(6, 2), compute='_deliver_compute')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept',string="Warehouse")

    def _compute_subtotal(self):
        print(self)
        self.subtotal_nodb = self.unit_price * self.quantity

    @api.onchange('unit_price', 'quantity')
    def _compute_sub_onchange(self):
        self.subtotal_onchange = self.unit_price * self.quantity

    @api.depends('unit_price', 'quantity')
    def _compute_sub_ondepends(self):
        for record in self:
            record.subtotal_ondepends = record.unit_price * record.quantity

    def _deliver_compute(self):

            for data in self:
                if data.stock_move_ids:
                    stock_tot = 0
                    for move in data.stock_move_ids:
                        stock_tot += move.qty_delivered
                    data.delivered_qty = stock_tot
                else:
                    data.delivered_qty = 0
