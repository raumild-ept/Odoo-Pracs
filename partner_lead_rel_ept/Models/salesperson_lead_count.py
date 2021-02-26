from odoo import fields, models, api


class SalespersonLeadCount(models.Model):
    _name = 'salesperson.lead.count'
    _description = 'Salespersons Leads and their details.'

    name = fields.Many2one(string='Name',comodel_name='res.users')
    customer_id = fields.Many2one(comodel_name='partner.lead.rel',string='Salesperson')
    total_pipelines = fields.Integer(compute="_compute_total",string='Count Of Pipelines')
    total_revenue = fields.Float(compute="_compute_total",digits=(6,2),string='Total Revenue')
    total_quotations = fields.Integer(compute="_compute_quots",string='Count Of Quotations')
    total_saleorders = fields.Integer(compute="_compute_quots",string='Count Of Sale Orders')
    total_order_amount = fields.Float(compute="_compute_quots",string='Total Amount',digits=(6,2))
    success_percentage = fields.Float(compute="_success_percentage",string='Success Ratio',digits=(6,2))

    @api.onchange('name')
    def _compute_total(self):
        for record in self:
            temp_tot_rev = 0
            total_pipelines = self.env['crm.lead'].search([('user_id','=',record.name.id),
                                                           ('partner_id','=',record.customer_id.partner_id.id)])
            record.total_pipelines = len(total_pipelines)

            for pipe in total_pipelines:
                if pipe.stage_id.id == 4:
                    temp_tot_rev += pipe.expected_revenue
            record.total_revenue = temp_tot_rev

    @api.onchange('name')
    def _compute_quots(self):
        for record in self:
            temp=0
            record.total_quotations = self.env['sale.order'].search_count([('user_id','=',record.name.id),
                                                                           ('partner_id', '=', record.customer_id.partner_id.id),
                                                               ('state','in',['draft','sent'])])
            total_sales = self.env['sale.order'].search([('user_id','=',record.name.id),
                                                         ('partner_id', '=', record.customer_id.partner_id.id),
                                                         ('state','in',['sale','done'])])
            record.total_saleorders = len(total_sales)
            for so in total_sales:
                temp += so.amount_untaxed
            record.total_order_amount = temp

    @api.onchange('name')
    def _success_percentage(self):
        for record in self:
            if record.total_revenue != 0:
                record.success_percentage = record.total_order_amount * 100 / record.total_revenue
            else:
                record.success_percentage = 0