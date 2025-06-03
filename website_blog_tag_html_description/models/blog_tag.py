from odoo import models, fields, _


class BlogTag(models.Model):
    _inherit = "blog.tag"

    html_description = fields.Html(
        string="HTML Description for Website",
        translate=True,
        help="Description shown in frontend when viewing the page of a single tag",
    )
