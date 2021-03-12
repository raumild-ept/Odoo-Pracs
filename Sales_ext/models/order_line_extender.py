from odoo import fields, models, api
from datetime import timedelta


class OrderLineExtender(models.Model):
    _inherit = 'sale.order.line'

    deposit_line_ids = fields.One2many('sale.order.line','parent_line_id', string="Deposit Line")
    parent_line_id = fields.Many2one('sale.order.line', string='Parent Line')
    is_deposit_line = fields.Boolean(string="Is Deposit Line",default = False)
    warehouse_manual_id = fields.Many2one(comodel_name='stock.warehouse',store=True,string='Warehouse',readonly = False)



    # def _prepare_procurement_values(self, group_id=False):
    #     """ Prepare specific key for moves or other components that will be created from a stock rule
    #     comming from a sale order line. This method could be override in order to add other custom key that could
    #     be used in move/po creation.
    #     """
    #     values = super(OrderLineExtender, self)._prepare_procurement_values(group_id)
    #     self.ensure_one()
    #     # Use the delivery date if there is else use date_order and lead time
    #     date_deadline = self.order_id.commitment_date or (self.order_id.date_order + timedelta(days=self.customer_lead or 0.0))
    #     date_planned = date_deadline - timedelta(days=self.order_id.company_id.security_lead)
    #     values.update({
    #         'group_id': group_id,
    #         'sale_line_id': self.id,
    #         'date_planned': date_planned,
    #         'date_deadline': date_deadline,
    #         'route_ids': self.route_id,
    #         'warehouse_id': values['warehouse_id'] or self.order_id.warehouse_id or False,
    #         'partner_id': self.order_id.partner_shipping_id.id,
    #         'product_description_variants': self._get_sale_order_line_multiline_description_variants(),
    #         'company_id': self.order_id.company_id,
    #     })
    #     return values


    # def unlink(self):
    #         browse = self.deposit_line_ids
    #         if browse:
    #             super(OrderLineExtender, browse).unlink()
    #         super(OrderLineExtender,self).unlink()

    def _prepare_procurement_values(self, group_id = False):
        values = super(OrderLineExtender, self)._prepare_procurement_values(group_id)
        values['warehouse_id'] = self.warehouse_manual_id
        return values


