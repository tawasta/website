from odoo import fields, models


class BlogBlog(models.Model):
    _inherit = "blog.blog"
    _order = "sequence, name"

    sequence = fields.Integer()
