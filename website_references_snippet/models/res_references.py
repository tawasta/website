from odoo import models, fields


class ResReferences(models.Model):
    _name = 'res.references'
    _description = 'References'

    name = fields.Char()
    description = fields.Text()
    image = fields.Binary()