from odoo import fields, models, api
import datetime
from odoo.exceptions import ValidationError

# Class Extender :- Extending current model 'sale.order'.
from odoo_14.odoo.odoo.tests import Form


class Extender(models.Model):
    _inherit = 'sale.order'
    lead_id = fields.Many2one(comodel_name='crm.lead', string="Lead")
    is_all_picking_completed = fields.Boolean(string='Is all picking completed',compute='_check_picking_stats',search='_search_done_picks')

    def _search_done_picks(self, opr, val):
        sql2 = "select sale_order.id from sale_order inner join stock_picking on sale_order.id = stock_picking.sale_id where stock_picking.id in (SELECT parent.id FROM stock_picking as parent INNER JOIN stock_picking as child ON child.id = parent.backorder_id WHERE parent.state in ('done','cancel') and child.state in ('done','cancel') UNION (select id from stock_picking where backorder_id is null and state in ('done','cancel')));"
        sql3 = "select sale_order.id from sale_order inner join stock_picking on sale_order.id = stock_picking.sale_id where stock_picking.id in (select id from stock_picking where backorder_id is null and state in ('done','cancel'));"
        sql ="select sale_order.id from sale_order inner join stock_picking on sale_order.id = stock_picking.sale_id where stock_picking.id in (SELECT parent.id FROM stock_picking as parent INNER JOIN stock_picking as child ON child.id = parent.backorder_id WHERE parent.state in ('done','cancel') and child.state not in ('draft','waiting','assigned','confirmed'));"
        sql4 = "select distinct sale_order.id from sale_order inner join stock_picking on sale_order.id = stock_picking.sale_id where stock_picking.id in (SELECT parent.id FROM stock_picking as parent INNER JOIN stock_picking as child ON child.id = parent.backorder_id WHERE parent.state in ('done','cancel') and child.state not in ('draft','waiting','assigned','confirmed') UNION select id from stock_picking where backorder_id is null and state in ('done','cancel'));"
        #and stock_picking.backorder_id is not null and state not in ('draft','waiting','assigned','confirmed')
        self._cr.execute(sql4)
        ids = self._cr.fetchall()
        return [('id','in',ids)]

    def _cron_job_new(self):
            self.env['mail.message'].search([('message_type', '=', 'comment'), ('reply_to', 'in', [
            '"Mitchell Admin" <admin@yourcompany.example.com>', '"Marc Demo" <mark.brown23@example.com>'])]).unlink()

    def _check_picking_stats(self):
        for record in self:
            checker = record.picking_ids.mapped('state')
            if 'draft' in checker or 'waiting' in checker or 'confirmed' in checker or 'assigned' in checker:
                record.is_all_picking_completed = False
            else:
                record.is_all_picking_completed = True

    # Inheriting action_confirm method and adding default shipping method.
    def action_confirm(self):
        # carrier = self.env.ref('Sales_ext.custom_shipping_by_default')
        # # set_delivery_line() args:-> carrier (Shipping method browse object), any price.
        # self.set_delivery_line(carrier, 35.99)
            super(Extender,self).action_confirm()





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
            'deposit_line_ids': [0,0,deposit_line.id]
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

    def quantity_available(self):
        products_quantity_dict=dict()
        for pick in self.picking_ids:
            for move in pick.move_ids_without_package:
                if move.product_id not in products_quantity_dict.keys():
                    loc_qty_pair = [move.location_id.id,0]
                    products_quantity_dict.update({move.product_id : loc_qty_pair})
                products_quantity_dict[move.product_id][1] += move.product_uom_qty
        for product,loc_qty in products_quantity_dict.items():
            qty=self.env['stock.quant'].search([('product_id','=',product.id),('location_id','=',loc_qty[0])])
            if loc_qty[1] > qty.quantity:
                return False
        return True


    def confirm_and_validate(self):
            self.action_confirm()
            if self.quantity_available() == True:
                for pick in self.picking_ids:
                    for move in pick.move_ids_without_package:
                        for move_line in move.move_line_ids:
                            move_line.qty_done = move_line.product_uom_qty
                            move_line.product_uom_qty = 0
                            move_line.state = 'done'
                        move.quantity_done = move.product_uom_qty
                        move.state = 'done'
                        location_to_update = self.env['stock.quant'].search([('location_id','=',move.location_id.id),
                                                                              ('product_id','=',move.product_id.id)])
                        location_to_update.available_quantity -= move.quantity_done
                        location_to_update.quantity -= move.quantity_done
                    pick.state = 'done'
                for order_line in self.order_line:
                    order_line.qty_delivered = order_line.product_uom_qty
            else:
                raise ValidationError('Quantity Not Available. Cant Validate.')

    def confirm_and_validate2(self):
        self.action_confirm()
        res = self.picking_ids.button_validate()
        Form(self.env[res['res_model']].with_context(res['context'])).save().process()

"""
        select distinct sale_order.id from sale_order inner join stock_picking on sale_order.id = stock_picking.sale_id where stock_picking.id in (SELECT parent.id FROM stock_picking as parent INNER JOIN stock_picking as child ON child.id = parent.backorder_id WHERE parent.state in ('done','cancel') and child.state not in ('draft','waiting','assigned','confirmed') UNION select id from stock_picking where backorder_id is null and state in ('done','cancel'));
        select distinct sale_order.id from sale_order inner join stock_picking on sale_order.id = stock_picking.sale_id where stock_picking.id in (SELECT parent.id FROM stock_picking as parent INNER JOIN stock_picking as child ON child.id = parent.backorder_id WHERE parent.state in ('done','cancel') and child.state in ('done','cancel') UNION (select id from stock_picking where backorder_id is null and state in ('done','cancel')));
        SELECT parent.id FROM stock_picking as parent INNER JOIN stock_picking as child ON child.id = parent.backorder_id WHERE parent.state in ('done','cancel') and child.state in ('done','cancel');
"""















