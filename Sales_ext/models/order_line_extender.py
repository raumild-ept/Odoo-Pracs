from odoo import fields, models, api


class OrderLineExtender(models.Model):
    _inherit = 'sale.order.line'

    deposit_line_ids = fields.One2many('sale.order.line','parent_line_id', string="Deposit Line")
    parent_line_id = fields.Many2one('sale.order.line', string='Parent Line')
    is_deposit_line = fields.Boolean(string="Is Deposit Line",default = False)


    # def unlink(self):
    #         browse = self.deposit_line_ids
    #         if browse:
    #             super(OrderLineExtender, browse).unlink()
    #         super(OrderLineExtender,self).unlink()


