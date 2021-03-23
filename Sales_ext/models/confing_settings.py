from odoo import fields, models


class ResConfigSettingsExt(models.TransientModel):
    _inherit = 'res.config.settings'

    config_shipping_id = fields.Many2one(related='company_id_ept.def_shipping_id',
                                         readonly=False,
                                         comodel_name='product.product',
                                         domain=[('is_shipping', '=', True)])

    config_shipping2_id = fields.Many2one(related='company_id_ept.def_shipping_id',
                                          readonly=False,
                                          comodel_name='product.product',
                                          config_parameter='sale.default_shipping_id',
                                          domain=[('is_shipping', '=', True)])

    company_id_ept = fields.Many2one(comodel_name='res.company')

    partner_ept_id = fields.Many2one(comodel_name='res.partner',
                                     related='company_id_ept.partner_ept_id',
                                     readonly=False)

    default_day_ept = fields.Selection(selection=[('Sunday', 'Sunday'),
                                                  ('Monday', 'Monday'),
                                                  ('Tuesday', 'Tuesday')],
                                       default='Sunday',
                                       default_model='res.company')

    group_tesla_manager = fields.Boolean(implied_group='Sales_ext.group_tesla_manager')
    module_spotify_connector = fields.Boolean()

    def execute(self):
        res = super(ResConfigSettingsExt, self).execute()
        group_id = self.env.ref('Sales_ext.group_tesla_manager')
        if self.group_tesla_manager == True:
            self.env.user.write({'groups_id': [(4, group_id.id)]})
        return res

    def _get_default_group(self):
        self.group_tesla_manager = True if self.env.user.has_group('Sales_ext.group_tesla_manager') else False


class ProductExt(models.Model):
    _inherit = 'product.template'

    is_shipping = fields.Boolean(default=False, string='Is Shipping Method',
                                 domain=[('type', '=', 'service')])


class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    def_shipping_id = fields.Many2one(comodel_name='product.product',
                                      domain=[('is_shipping', '=', True)])

    partner_ept_id = fields.Many2one(comodel_name='res.partner',
                                     string='Ept Partner')

    day_ept = fields.Selection(selection=[('Sunday', 'Sunday'),
                                          ('Monday', 'Monday'),
                                          ('Tuesday', 'Tuesday')])
