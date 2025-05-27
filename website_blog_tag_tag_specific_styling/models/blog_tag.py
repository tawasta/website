from odoo import models, fields, _


class BlogTag(models.Model):
    _inherit = "blog.tag"

    css_classes = fields.Char(
        string="CSS Classes",
        help="e.g. 'my-class my-another-class', can be used in website builder's "
        "CSS editor to style the content",
    )
