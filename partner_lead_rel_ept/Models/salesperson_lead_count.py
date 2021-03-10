from odoo import fields, models, api


class SalespersonLeadCount(models.Model):
    _name = 'salesperson.lead.count'
    _description = 'Salesperson Lead Count'

    name = fields.Many2one(string='Name', comodel_name='res.users',help='Sales Person')
    customer_id = fields.Many2one(comodel_name='partner.lead.rel', string='Salesperson',help='Customer')
    total_pipelines = fields.Integer(compute="_compute_total", string='Total Pipelines',help='Number of pipelines by the salesperson.')
    total_revenue = fields.Float(compute="_compute_total", digits=(6, 2), string='Total Expected Revenue',help='Total expected revenue by the salesperson.')
    total_quotations = fields.Integer(compute="_compute_total", string='Total Quotations',help='Number of quotations by the salesperson.')
    total_saleorders = fields.Integer(compute="_compute_total", string='Total Sale Orders',help='Number of sale orders by the salesperson.')
    total_order_amount = fields.Float(compute="_compute_total", string='Total Amount', digits=(6, 2),help='Total amount by the salesperson.')
    success_percentage = fields.Float(compute="_compute_total", string='Success Ratio', digits=(6, 2),help='Success ration of the salesperson.')

    @api.onchange('name')
    def _compute_total(self):
        for record in self:
            total_pipelines = record.customer_id.get_lead_ids()
            total_pipelines = total_pipelines.filtered(lambda x:x if x.user_id.id == record.name.id else False )
            record.total_pipelines = len(total_pipelines)
            pipes = total_pipelines.filtered(lambda x:x if x.stage_id.id == 4 else False)
            record.total_revenue=sum(pipes.mapped('expected_revenue'))

            #To count total quotations and total sale orders and total amount(untaxed).
            record.total_quotations = self.env['sale.order'].search_count(
                ['|', ('partner_id', 'in', record.customer_id.partner_contacts_ids.ids),
                 ('partner_id', '=',
                  record.customer_id.partner_id.id),
                 ('lead_id','in',total_pipelines.ids),
                 ('user_id', '=', record.name.id)])
            total_sales = self.env['sale.order'].search(
                ['|', ('partner_id', 'in', record.customer_id.partner_contacts_ids.ids),
                 ('partner_id', '=', record.customer_id.partner_id.id),
                 ('lead_id', 'in', total_pipelines.ids),
                 ('user_id', '=', record.name.id),
                 ('state', 'in', [ 'done','sale'])])
            record.total_saleorders = len(total_sales)
            untaxed_amounts_list =total_sales.mapped('amount_untaxed')
            record.total_order_amount = sum(untaxed_amounts_list)

            #To count success percentage.
            if record.total_revenue != 0:
                record.success_percentage = record.total_order_amount * 100 / record.total_revenue
            else:
                if record.total_order_amount:
                    record.success_percentage = 100
                else:
                    record.success_percentage = 0
