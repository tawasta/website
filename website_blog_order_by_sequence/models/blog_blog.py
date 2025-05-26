from odoo import models, fields, _


class BlogBlog(models.Model):
    _inherit = "blog.blog"
    _order = "sequence, name"

    sequence = fields.Integer()
