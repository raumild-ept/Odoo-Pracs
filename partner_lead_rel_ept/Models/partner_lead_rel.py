from odoo import fields, models, api


class PartnerLeadRel(models.Model):
    _name = 'partner.lead.rel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Partner Lead Relationship.'

    name = fields.Char(string='Name', readonly=True, default='Seq_#####')
    name2=fields.Char(string='Name',default = 'seq')
    from_date = fields.Date(string='From Date',help="Enter start date.")
    to_date = fields.Date(string='To Date',help="Enter end date.")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', domain="[('is_company','=',True)]",help='Enter Partner.')
    partner_contacts_ids = fields.Many2many(comodel_name='res.partner',
                                            string='Partner Contacts',
                                            domain="[('is_company','=',False),('parent_id','=',partner_id)]"
                                            ,help='Enter Partners Contacts.'
                                            )
    salesperson_lead_count_ids = fields.One2many(comodel_name='salesperson.lead.count',inverse_name='customer_id',string='Sales Leads',help='Salespersons and their states.'
                                                 )
    lead_ids = fields.Many2many(compute='_compute_leads',comodel_name='crm.lead', string='Opportunities',help="Leads and Opportunities.")
    total_revenue = fields.Float(compute='_compute_revenue', digits=(6, 2), string='Total Revenue',help='Total Generated Revenue.')
    leads_count = fields.Integer(compute="lead_count",help='Number of leads by the salesperson.')
    paid_orders_count = fields.Integer(compute="lead_count",help='Number of paid orders by the salesperson.')
    sample_field = fields.Boolean(string="Loading Salesperson Lines", compute='load_pipe')

    @api.onchange('partner_id','from_date','to_date','partner_contacts_ids')
    def _compute_leads(self):
        for record in self:
            if record.partner_id:
                record.lead_ids = record.get_lead_ids()

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('partner.lead.rel') or '/'
        vals['name'] = seq
        return super(PartnerLeadRel, self).create(vals)

    def get_pipeline_details(self):
        self.env['salesperson.lead.count'].search([('customer_id', '=', self.id)]).unlink()
        cust_leads = self.env['crm.lead'].search(['|',('partner_id', '=', self.partner_id.id),
                                                  ('partner_id','in',self.partner_contacts_ids.ids)])
        salespersons = cust_leads.mapped('user_id')
        for salesperson in salespersons:
            self.env['salesperson.lead.count'].create({
                'customer_id': self.id,
                'name': salesperson.id
            })

    def load_pipe(self):
        for record in self:
            if not record.sample_field:
                record.get_pipeline_details()
                record.sample_field = True

    def _compute_revenue(self):
        for record in self:
            record.total_revenue = sum(record.mapped('salesperson_lead_count_ids.total_order_amount'))

    def get_lead_ids(self):
        if self.from_date:
            if self.to_date:
                load_ids = self.env['crm.lead'].search(['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_contacts_ids.ids),
                                                        ('date_deadline', '>=', self.from_date),
                                                        ('date_deadline', '<=', self.to_date)])
            else:
                load_ids = self.env['crm.lead'].search(['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_contacts_ids.ids),
                                                        ('date_deadline', '>=', self.from_date)])
        else:
            load_ids = self.env['crm.lead'].search(
                ['|', ('partner_id', '=', self.partner_id.id), ('partner_id', 'in', self.partner_contacts_ids.ids)])
        return load_ids

    def get_leads(self):
        load_ids = self.get_lead_ids()
        action = self.env['ir.actions.act_window']._for_xml_id('crm.crm_lead_action_pipeline')
        if load_ids:
            if len(load_ids) > 1:
                action['domain'] = [('id', 'in', load_ids.ids)]
            elif len(load_ids) == 1:
                form_view = [(self.env.ref('crm.crm_lead_view_form').id, 'form')]
                action['views'] = form_view
                action['res_id'] = load_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def get_paid_orders(self):
        load_ids = self.get_lead_ids()
        sale_order_ids = self.env['sale.order'].search([('lead_id', 'in', load_ids.ids),
                                                        ('invoice_ids.payment_state', 'in', ['paid','partial','in_payment']),
                                                        ]).ids
        action = self.env['ir.actions.act_window']._for_xml_id('partner_lead_rel_ept.action_sale_order_tree_all_new')
        if load_ids:
            if len(sale_order_ids) > 1:
                action['domain'] = [('id', 'in', sale_order_ids)]
                action['views'] = [(self.env.ref('partner_lead_rel_ept.view_order_tree_new2').id, 'tree'),(self.env.ref('sale.view_order_form').id, 'form')]
            elif len(sale_order_ids) == 1:
                form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
                action['views'] = form_view
                action['res_id'] = sale_order_ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def lead_count(self):
        for record in self:
            leads = record.get_lead_ids()
            record.leads_count = len(leads.ids)
            record.paid_orders_count = self.env['sale.order'].search_count([('lead_id', 'in', leads.ids),
                                                                            ('invoice_ids.payment_state', 'in', ['paid','partial','in_payment']),
                                                                            ])
