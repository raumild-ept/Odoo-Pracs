from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Picking(models.Model):
    _name = 'stock.picking.ept'
    _description = 'Stock Picking'

    name = fields.Char(string = "Name",readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner.sales.ept',string="Partner ID",
                                 domain=[('address_type','=','Shipping')])
    parent_id = fields.Many2one(comodel_name='stock.picking.ept',string="Parent ID")
    state = fields.Selection(selection=[('Draft','Draft'),
                                        ('Validated','Validated'),
                                        ('Cancelled','Cancelled')],string= "State")
    sale_order_id = fields.Many2one(comodel_name='sale.orders.ept',string="Sale Order ID",help="Sale Order ID")
    order_line_ids = fields.One2many(comodel_name='stock.move.ept',inverse_name='picking_id',string='Order Lines')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('picking.name.ept')
        vals['name']=seq
        return super(Picking, self).create(vals)

    def validate_delivery_order(self):
        validation_list = list()
        self.state = "Validated"
        for line in self.order_line_ids:
            if line.qty_to_deliver != line.qty_delivered:
                if line.qty_to_deliver > line.qty_delivered:
                    validation_list.append(line)
                elif line.qty_to_deliver < line.qty_delivered:
                    raise ValidationError("Cant deliver more than asked for...")
            line.state = 'Done'

        if validation_list:
            new_picking = self.create({'parent_id':self.id,
                                 'partner_id':self.partner_id.id,
                                 'state':'Validated',
                                 'sale_order_id':self.sale_order_id.id})


            for line in validation_list:
                self.env['stock.move.ept'].create({
            'name': line.name,
            'product_id': line.product_id.id,
            'uom_id': line.uom_id.id,
            'source_location_id': line.source_location_id.id,
            'destination_location_id': line.destination_location_id.id,
            'qty_to_deliver': line.qty_to_deliver - line.qty_delivered,
            'state': 'Draft',
            'sale_line_id': line.sale_line_id.id,
            'stock_inventory_id': line.stock_inventory_id.id,
            'picking_id': new_picking.id
            })
        elif not validation_list:
            self.sale_order_id.state = 'Done'


