from odoo import fields, models, api


class SaleOrder(models.Model):
    _name = "sale.orders.ept"
    _description = "Sale Orders"
    _rec_name = "order_no"

    order_no = fields.Char(string="Order No ", copy=False)
    customer_id = fields.Many2one(comodel_name='res.partner.sales.ept',
                                  string="Customer ")
    invoice_customer_id = fields.Many2one(comodel_name='res.partner.sales.ept',
                                          string="Invoice Customer ")
    shipping_customer_id = fields.Many2one(comodel_name='res.partner.sales.ept',
                                           string="Shipping Customer ")
    sale_order_date = fields.Date(string="Date")
    order_line_ids = fields.One2many(comodel_name='sale.order.line.ept',
                                     inverse_name='order_no_id',
                                     string="Order Line ")
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson ",
                                     default=lambda self: self.env.user.id)
    state = fields.Selection(selection=[('Draft', 'Draft'),
                                        ('Confirmed', 'Confirmed'),
                                        ('Done', 'Done'),
                                        ('Cancelled', 'Cancelled')],
                             string="State ", default='Draft')
    total_weight = fields.Float(compute='_compute_total_weight_and_volume',
                                string="Weight ")
    total_volume = fields.Float(string="Volume ")
    lead_id = fields.Many2one(comodel_name='crm.lead.ept2',
                              string='Lead ID ', help='Enter Lead ID')
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse.ept',
                                   string="Warehouse ",
                                   help='Select Warehouse')
    picking_ids = fields.One2many(comodel_name='stock.picking.ept',
                                  inverse_name='sale_order_id',
                                  string="Picking IDs ",
                                  readonly=True)
    moves_count = fields.Integer(compute="_compute_count")
    picks_count = fields.Integer(compute="_compute_count")
    total_tax = fields.Float(compute="_compute_total_tax",
                             string="Total Tax ", store=True)
    total_amount = fields.Float(compute="_compute_total_amount",
                                string="Total Amount ", store=True)
    subtotal_without_tax = fields.Float(compute="_compute_sub", store=False)

    def list_age_equal(self):
        action = self.env.ref('Sales.action_res_partners_sales_ept')
        to_show = self.env['res.partner.sales.ept'].search([('age_calculate', '=', 20)
                                                            ])

        action['domain'] = [('id', 'in', to_show.ids)]
        action['views'] = [(self.env.ref('Sales.view_res_partner_sales_tree').id, 'tree'),
                           (self.env.ref('Sales.view_res_partner_sales_form').id, 'form')]
        return action

    @api.depends('order_line_ids')
    def _compute_sub(self):
        for record in self:
            line_total = 0
            for line in record.order_line_ids:
                line_total += line.subtotal_without_tax
            record.subtotal_without_tax = line_total

    def _compute_total_weight_and_volume(self):
        temp_weight = 0
        temp_volume = 0
        for line in self.order_line_ids:
            temp_weight += (float(line.product_name_id.weight) * float(line.quantity))
            temp_volume += (float(line.product_name_id.volume) * float(line.quantity))
        self.total_weight = temp_weight
        self.total_volume = temp_volume

    @api.onchange('customer_id')
    def _default_address(self):
        if self.customer_id:
            invoice = list(filter(lambda child:
                                  child if child.address_type == 'Invoice' else False,
                                  list(self.customer_id.child_ids)))
            shipping = list(filter(lambda child:
                                   child if child.address_type == 'Shipping' else False,
                                   list(self.customer_id.child_ids)))
            if invoice:
                self.invoice_customer_id = invoice[0]
            if shipping:
                self.shipping_customer_id = shipping[0]

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('sale.order.no') or 'none'
        vals['order_no'] = seq
        return super(SaleOrder, self).create(vals)

    def create_delivery_order(self):
        order = self.env['stock.picking.ept'].create({
            'partner_id': self.shipping_customer_id.id,
            'state': 'Draft',
            'sale_order_id': self.id
        })
        self.create_stock_moves(order)

    def create_stock_moves(self, order):
        for line in self.order_line_ids:
            self.env['stock.move.ept'].create({
                'name': line.product_name_id.name,
                'product_id': line.product_name_id.id,
                'uom_id': line.uom_id.id,
                'source_location_id': self.warehouse_id.stock_location_id.id,
                'destination_location_id': (self.env['stock.location.ept'].search(
                    [('location_type', '=', 'Customer')])).id,
                'qty_to_deliver': line.quantity,
                'state': 'Draft',
                'sale_line_id': line.id,
                'picking_id': order.id})

    def _compute_count(self):
        for record in self:
            count = 0
            record.picks_count = len(record.picking_ids)
            for pick in record.picking_ids:
                temp_count = len(pick.order_line_ids.ids)
                count += temp_count
            record.moves_count = count

    def picking_ids_list(self):
        action = self.env['ir.actions.actions']._for_xml_id('Sales.action_picking')
        pick_id_list = self.picking_ids.ids
        if pick_id_list:
            if len(pick_id_list) > 1:
                action['domain'] = [('id', 'in', pick_id_list)]
            elif len(pick_id_list) == 1:
                form_view = [(self.env.ref('Sales.view_form_picking').id, 'form')]
                action['views'] = form_view
                action['res_id'] = pick_id_list[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def stock_moves_list(self):
        action = self.env['ir.actions.actions']._for_xml_id("Sales.action_move")
        stock_moves = self.picking_ids.order_line_ids.ids
        if stock_moves:
            if len(stock_moves) > 1:
                action['domain'] = [('id', 'in', stock_moves)]
            elif len(stock_moves) == 1:
                form_view = [(self.env.ref('Sales.view_form_move').id, 'form')]
                action['views'] = form_view
                action['res_id'] = stock_moves[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def confirm_sale_order(self):
        for line in self.order_line_ids:
            line.state = 'Confirmed'
        self.state = 'Confirmed'
        transport_dict = dict()

        for line in self.order_line_ids:
            if line.warehouse_id in transport_dict.keys():
                transport_dict[line.warehouse_id].append(line.id)
            elif line.warehouse_id not in transport_dict.keys():
                transport_dict.update({line.warehouse_id: [line.id]})

        for warehouse, order_lines in transport_dict.items():
            order = self.env['stock.picking.ept'].create({
                'partner_id': self.shipping_customer_id.id,
                'state': 'Draft',
                'sale_order_id': self.id
            })

            for order_line in order_lines:
                line = self.env['sale.order.line.ept'].search([('id', '=', order_line)])
                self.env['stock.move.ept'].create({
                    'name': line.product_name_id.name,
                    'product_id': line.product_name_id.id,
                    'uom_id': line.uom_id.id,
                    'source_location_id': warehouse.stock_location_id.id,
                    'destination_location_id': (self.env['stock.location.ept'].search(
                        [('location_type', '=', 'Customer')])).id,
                    'qty_to_deliver': line.quantity,
                    'state': 'Draft',
                    'sale_line_id': line.id,
                    'picking_id': order.id})

    @api.depends('order_line_ids')
    def _compute_total_tax(self):
        for record in self:
            tax = 0
            for line in record.order_line_ids:
                tax += line.tax_total
            record.total_tax = tax

    @api.depends('order_line_ids')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.subtotal_without_tax + record.total_tax
