from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'crm.lead.line.ept'
    _description = 'CRM Lead Line'
    _rec_name = "lead_id"

    product_id = fields.Many2one(comodel_name='product.ept.sales',string = "Product")
    sell_qty = fields.Float(string="Expected Sale Quantity",digits = (6,2),help="Expected Sale Quantity.")
    uom_id = fields.Many2one(comodel_name='product.uom.ept',string="UOM",help='Enter UOM')
    lead_id = fields.Many2one(comodel_name='crm.lead.ept2',string='Lead')

    @api.onchange('product_id')
    def on_product_change(self):
        if self.product_id:
            self.uom_id = self.product_id.product_uom_id
            self.sell_qty = 1