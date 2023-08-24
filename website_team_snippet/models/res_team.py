from odoo import fields, models


class ResTeam(models.Model):
    _name = "res.team"
    _description = "Team"

    name = fields.Char()
    professional_title = fields.Char(string="Professional title")

    description = fields.Text()
    image = fields.Binary()
