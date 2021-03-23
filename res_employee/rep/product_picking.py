from odoo import api , fields , models , SUPERUSER_ID , _

class ProductPicking(models.AbstractModel):
    _name = 'report.stock_extended.product_picking_template_report'

    @api.model
    def _get_report_values(self,docids,data=None):
        docs = self.env['stock.picking'].browse(docids)
        products=docs.product_id


        return {
            'doc_ids': docids,
            'docs': docs,
            'products': products
        }