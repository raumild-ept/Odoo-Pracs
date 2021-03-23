from odoo import fields, models


class Inventory(models.Model):
    _name = 'stock.inventory.ept'
    _description = 'Stock Inventory'

    name = fields.Char(string='Name ')
    state = fields.Selection(selection=[('Draft', 'Draft'),
                                        ('In Progress', 'In Progress'),
                                        ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')],
                             string='State ', default='Draft')
    location_id = fields.Many2one(comodel_name='stock.location.ept', string="Location ID")
    inventory_line_ids = fields.One2many(comodel_name='stock.inventory.line.ept',
                                         inverse_name='inventory_id', string='Inventory Lines')

    def start_inventory(self):
        self.state = 'In Progress'
        for inventory_line in self.inventory_line_ids:
            inventory_line.available_qty = inventory_line.with_context(loc=self.location_id.id). \
                product_id.product_stock

    def validate_inventory(self):
        self.state = "Done"
        for inventory_line in self.inventory_line_ids:
            if inventory_line.difference != 0:
                inventory_loss_loc = self.env['stock.location.ept']. \
                    search([('location_type', '=', 'Inventory Loss')])
                if inventory_line.difference > 0:
                    location = [inventory_loss_loc.id, self.location_id.id]
                else:
                    location = [self.location_id.id, inventory_loss_loc.id]

                self.env['stock.move.ept'].create({
                    'name': inventory_line.product_id.name,
                    'product_id': inventory_line.product_id.id,
                    'uom_id': inventory_line.product_id.product_uom_id.id,
                    'source_location_id': location[0],
                    'destination_location_id': location[1],
                    'qty_to_deliver': abs(inventory_line.difference),
                    'qty_delivered': abs(inventory_line.difference),
                    'state': 'Done',
                })
                inventory_line.available_qty = inventory_line.counted_product_qty
