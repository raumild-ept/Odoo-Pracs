from odoo import fields, models, api


class SalesExt(models.Model):
    _inherit = 'sale.order'

    total_paid_invoice_amount = fields.Float(compute = '_compute_amounts',string='Paid Invoice Amount',default = 10)
    remaining_amount = fields.Float(compute = '_compute_amounts',string='Remaining Amount',default = 8)

    def _compute_amounts(self):
        for record in self:
            invoices = self.env['account.move'].search([('id','in',record.invoice_ids.ids),
                                                        ('state','=','posted')])
            to_sum = invoices.mapped('amount_total')
            record.total_paid_invoice_amount = sum(to_sum)
            record.remaining_amount = record.amount_total - record.total_paid_invoice_amount






