from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'crm.team.ept'
    _description = 'CRM Lead.'

    name = fields.Char(string = "Name",help="Enter Name")
    team_leader_id=fields.Many2one(comodel_name='res.users',string="Team Leader",help="Enter Team Leader.")

