from odoo import fields, models, api


# Class Extender :- Extending current model 'sale.order'.
from odoo_14.odoo.odoo.tests import Form


class Extender(models.Model):
    _inherit = 'sale.order'
    lead_id = fields.Many2one(comodel_name='crm.lead', string="Lead")

    # Inheriting action_confirm method and adding default shipping method.
    def action_confirm(self):
        carrier = self.env.ref('Sales_ext.custom_shipping_by_default')
        # set_delivery_line() args:-> carrier (Shipping method browse object), any price.
        self.set_delivery_line(carrier, 35.99)
        super(Extender, self).action_confirm()

    # Method to create deposit line.
    def create_deposit_line(self, line):
        deposit_line = self.env['sale.order.line'].create({
            'order_id': self.id,
            'product_id': line.product_id.deposit_product_id.id,
            'price_unit': line.product_id.deposit_product_id.list_price,
            'product_uom_qty': line.product_uom_qty * line.product_id.deposit_product_qty,
            'parent_line_id': line.id,
            'is_deposit_line': True
        })
        line.write({
            'deposit_line_ids': [deposit_line.id]
        })

    # Method to manage deposit lines of order_lines of model 'sale.order'
    def manage_deposit(self):
        order_line_ids = self.order_line.mapped('id')
        for line in self.order_line:
            if line.product_id.deposit_product_id:
                # If an order_line does not have any child deposit id than it will create
                # new deposit line.
                if not line.deposit_line_ids:
                    self.create_deposit_line(line)
                # If child deposit line exists than it will update deposit_product_qty.
                else:
                    for dep_line in line.deposit_line_ids:
                        dep_line.write({
                            'product_uom_qty': line.product_uom_qty * line.product_id.deposit_product_qty
                        })
            # Unlink-> If line is deposit line and its parent line is not present in orderlines than unlink that line.
            if line.is_deposit_line == True and line.parent_line_id.id not in order_line_ids:
                line.unlink()

    # Decorating with @api.model and inheriting create method.
    @api.model
    def create(self, vals):
        new = super(Extender, self).create(vals)
        # If product has default deposit product id than create deposit_line:
        for line in new.order_line:
            if line.product_id.deposit_product_id:
                new.create_deposit_line(line)
        return new

    def review_order_lines(self):
        products = self.order_line.filtered(lambda x: x.is_deposit_line == False and
                                               x.is_delivery == False).product_id
        order_lines = self.env['sale.order.line'].search(
            [('product_id', 'in', products.ids),('order_id.picking_ids.state', '=', 'assigned'),
             ('order_id.picking_ids.move_ids_without_package.product_id', 'in', products.ids),
             ('order_id.picking_ids.move_line_ids_without_package.state', 'in', ['assigned', 'partially_available'])])
        action = self.env['ir.actions.act_window']._for_xml_id('Sales_ext.action_sale_line2')
        action['domain'] = [('id', 'in', order_lines.ids)]
        return action

    def confirm_and_validate(self):
        for sale_order in self:
            super(Extender, sale_order).action_confirm()
            # for pick in sale_order.picking_ids:
            #     for move in pick.move_ids_without_package:
            #         for move_line in move.move_line_ids:
            #             move_line.qty_done = move_line.product_uom_qty
            #             move_line.product_uom_qty = 0
            #             move_line.state = 'done'
            #         move.quantity_done = move.product_uom_qty
            #         move.state = 'done'
            #         location_to_update = self.env['stock.quant'].search([('location_id','=',move_line.location_id.id),
            #                                                               ('product_id','=',move_line.product_id.id)])
            #         location_to_update.available_quantity -= move.quantity_done
            #         location_to_update.quantity -= move.quantity_done
            #     pick.state = 'done'
            # for order_line in sale_order.order_line:
            #     order_line.qty_delivered = order_line.product_uom_qty
            res = self.picking_ids.button_validate()
            Form(self.env[res['res_model']].with_context(res['context'])).save().process()

