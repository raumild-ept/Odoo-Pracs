from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Sales(models.TransientModel):
    _name = 'sale.order.team.ept'

    current_sales_team_id = fields.Many2one(comodel_name='crm.team')
    current_sales_person_id = fields.Many2one(comodel_name='res.users')
    sales_team_id = fields.Many2one(comodel_name='crm.team', default=lambda self: self.env.user.sale_team_id)
    sales_person_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user)

    def update_data(self):
        if self.sales_person_id not in self.sales_team_id.member_ids:
            raise ValidationError(_('Sales Person not in team.'))
        else:
            order = self.env['sale.order'].browse(self.env.context.get('active_id'))
            order.team_id, order.user_id = self.sales_team_id.id, self.sales_person_id.id
