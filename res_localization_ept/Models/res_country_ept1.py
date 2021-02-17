from odoo import api, models, fields, SUPERUSER_ID, _

class ResCountryEpt(models.Model):
    _name = "res.country1.ept"
    _description = "description of res.country.ept"
    _rec_name = "country"

    country = fields.Char(string="Country Name", required=True, help="Please enter country name.")
    c_code = fields.Char(string="Country Code", required=True, help="Please enter country code")
    state_ids = fields.One2many(comodel_name ="res.state1.ept",inverse_name="country_id", string="State Names")

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if args:
            if args[0][0] == 'country':
                dom = ['|']
                dom.append(args[0])
                dom.append(['c_code','ilike',args[0][2]])
                args = dom
        return super(ResCountryEpt, self)._search(args, offset, limit, order, count=count,
                                                  access_rights_uid=access_rights_uid)

