from odoo import api,fields,models


class LeadExtender(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        tag_xml = self.env.ref('Sales_ext.tad_id_data_to_sale_order')
        action = super(LeadExtender, self).action_new_quotation()
        action['context'].update({'default_lead_id':self.id,
                                  'default_tag_ids':[(6, 0, tag_xml.ids)]})
        return action

