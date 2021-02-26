from odoo import fields, models, api


class PartnerLeadRel(models.Model):
    _name = 'partner.lead.rel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Model for partner lead relationship.'

    name = fields.Char(string='Name', readonly=True, default='/')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', domain="[('is_company','=',True)]")
    partner_contacts_ids = fields.Many2many(comodel_name='res.partner',
                                            string='Partner Contacts',
                                            domain="[('is_company','=',False),('parent_id','=',partner_id)]"
                                            )
    salesperson_lead_count_ids = fields.One2many(comodel_name='salesperson.lead.count',
                                                 inverse_name='customer_id',
                                                 string='Sales Leads')
    lead_ids = fields.Many2many(comodel_name='crm.lead', string='Leads')
    total_revenue = fields.Float(compute='_compute_revenue', digits=(6, 2), string='Total Revenue')
    leads_count = fields.Integer(compute="lead_count")
    paid_orders_count = fields.Integer(compute="lead_count")

    # @api.onchange('partner_id')
    # def _compute_leads(self):
    #     for record in self:
    #         cust_leads = self.env['crm.lead'].search([('partner_id', '=', record.partner_id.id)
    #                                                ])
    #         list_to_append = []
    #         for cust_lead in cust_leads:
    #              = (0,0,cust_lead)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('partner.lead.rel') or '/'
        vals['name'] = seq
        return super(PartnerLeadRel, self).create(vals)

    def get_pipeline_details(self):
        cust_leads = self.env['crm.lead'].search([('partner_id', '=', self.partner_id.id)])
        salespersons = cust_leads.mapped('user_id')
        to_unlink = self.env['salesperson.lead.count'].search([('customer_id', '=', self.id)])
        for x in to_unlink:
            x.unlink()

        for salesperson in salespersons:
            self.env['salesperson.lead.count'].create({
                'customer_id': self.id,
                'name': salesperson.id
            })

    def _compute_revenue(self):
        for record in self:
            temp_rev = 0
            sales = record.mapped('salesperson_lead_count_ids')
            for sale in sales:
                temp_rev += sale.total_order_amount
            record.total_revenue = temp_rev

    def get_lead_ids(self):
        if self.from_date:
            if self.to_date:
                load_ids = self.env['crm.lead'].search([('partner_id', '=', self.partner_id.id),
                                                        ('date_deadline', '>=', self.from_date),
                                                        ('date_deadline', '<=', self.to_date)]).ids
            else:
                load_ids = self.env['crm.lead'].search([('partner_id', '=', self.partner_id.id),
                                                        ('date_deadline', '>=', self.from_date)]).ids


        else:
            load_ids = self.env['crm.lead'].search([('partner_id', '=', self.partner_id.id)]).ids

        return load_ids

    def get_leads(self):
        load_ids = self.get_lead_ids()
        action = self.env['ir.actions.act_window']._for_xml_id('crm.crm_lead_action_pipeline')
        action['domain'] = [('id', 'in', load_ids)]
        return action

    def get_paid_orders(self):
        load_ids = self.get_lead_ids()
        sale_order_ids = self.env['sale.order'].search([('lead_id', 'in', load_ids),
                                                        ('payment_term_id', '=', 1),
                                                        ('picking_ids.state', '!=', ['done', 'cancel'])]).ids

        action = self.env['ir.actions.act_window']._for_xml_id('partner_lead_rel_ept.action_sale_orders_partner_lead2')
        action['domain'] = [('id', 'in', sale_order_ids)]
        return action

    def lead_count(self):
        for record in self:
            leads = record.get_lead_ids()
            record.leads_count = len(leads)
            record.paid_orders_count = self.env['sale.order'].search_count([('lead_id', 'in', leads),
                                                                            ('payment_term_id', '=', 1),
                                                                            ('picking_ids.state', '!=',
                                                                             ['done', 'cancel'])])
