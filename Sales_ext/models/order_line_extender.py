from odoo import fields, models, api


class OrderLineExtender(models.Model):
    _inherit = 'sale.order.line'

    deposit_line_ids = fields.One2many('sale.order.line', 'parent_line_id',
                                       string="Deposit Line")
    parent_line_id = fields.Many2one('sale.order.line', string='Parent Line')
    is_deposit_line = fields.Boolean(string="Is Deposit Line", default=False)
    warehouse_manual_id = fields.Many2one(comodel_name='stock.warehouse', store=True,
                                          string='Warehouse', readonly=False)
    profit_percentage = fields.Float(compute='_compute_profit', digits=(6, 2),
                                     string='Profit Percentage', store=True)
    profit_margin = fields.Float(compute='_compute_profit', digits=(6, 2),
                                 string='Profit Margin', store=True)

    def _prepare_procurement_values(self, group_id=False):
        values = super(OrderLineExtender, self)._prepare_procurement_values(group_id)
        if self.warehouse_manual_id:
            values['warehouse_id'] = self.warehouse_manual_id
        return values

    @api.depends('price_subtotal')
    def _compute_profit(self):
        for line in self:
            sale_price = line.price_unit - (line.price_unit * line.discount / 100)
            cost_price = line.product_id.standard_price
            line.profit_margin = (sale_price - cost_price) * line.product_uom_qty
            if cost_price > 0:
                line.profit_percentage = ((line.profit_margin /
                                           line.product_uom_qty) / cost_price) * 100
            elif cost_price == 0:
                line.profit_percentage = 100
