from odoo import fields, models


class ResReferences(models.Model):
    _name = "res.references"
    _description = "References"
    _order = "sequence"

    name = fields.Char()
    description = fields.Text()
    image = fields.Binary()
    sequence = fields.Integer(string="Sequence")
