from odoo import api, models


class StockPickingReport(models.AbstractModel):
    _name = 'report.stock_extended.product_picking_template_report'

    def get_product_pick_list_dict(self, obj):
        products = obj.mapped('product_id')
        dict = {}
        for pick in obj:
            for line in pick.move_ids_without_package:
                if line.product_id in products:
                    if line.product_id in dict:
                        dict[line.product_id].append((pick, line.product_uom_qty))
                    else:
                        dict.update({
                            line.product_id: [(pick, line.product_uom_qty)]
                        })
        return dict

    @api.model
    def _get_report_values(self, docids, data=False):
        docs = self.env['stock.picking'].browse(docids)
        # dict = self.get_product_pick_list_dict(docs)
        # products = list(dict.keys())
        # pick_qty = list(dict.values())
        # i=0
        # lists = []
        # for pro in products:
        #     lists.append([pro,pick_qty[i]])
        #     i+=1
        # print(lists)
        # products =  docs.move_ids_without_package.mapped('product_id')
        products = docs.move_ids_without_package.mapped('product_id')
        return {
            'docs': docs,
            'products': products,
            'doc_ids': docids
        }
    #
    # @api.model
    # def _get_report_values(self,docids,data=None):
    #     docs = self.env['stock.picking'].browse(docids)
    #     products = docs.product_id
    #
    #     return {
    #         'doc_ids': docids,
    #         'docs': docs,
    #         'products': products
    #     }
