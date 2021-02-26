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
    tax_ids = fields.Many2many(comodel_name = "account.tax.ept", string="Taxes", help="Taxes")
    tax_total = fields.Float(compute="_compute_tax",string="Subtotal of  Tax",store=True)
    subtotal_without_tax = fields.Float(compute='_compute_subtotal_without_tax',string="Subtotal Without Tax",store = True)
    subtotal_tax = fields.Float(compute="_compute_subtotal_with_tax",string='Subtotal With Tax',store=True)

    @api.onchange('product_name_id')
    def on_product_select(self):
        if self.product_name_id:
            self.unit_price = self.product_name_id.sale_price
            self.quantity = 1
            self.uom_id = self.product_name_id.product_uom_id

    @api.depends('tax_total','subtotal_without_tax')
    def _compute_subtotal_with_tax(self):
        for record in self:
            record.subtotal_tax = record.tax_total + record.subtotal_without_tax

    @api.depends('quantity')
    def _compute_tax(self):
        for record in self:
            temp_tax = 0
            for tax in record.tax_ids:
                if tax.tax_amount_type == "Percentage":
                    temp_tax +=(record.quantity*record.unit_price)*tax.tax_value/100
                else:
                    temp_tax += tax.tax_value
            record.tax_total=temp_tax

    @api.depends('quantity','unit_price')
    def _compute_subtotal_without_tax(self):
        for record in self:
            record.subtotal_without_tax=record.quantity*record.unit_price

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
