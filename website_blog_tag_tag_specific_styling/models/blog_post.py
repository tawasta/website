from odoo import models, fields, api, _


class BlogPost(models.Model):
    _inherit = "blog.post"

    tags_css_classes = fields.Char(
        compute="_compute_css_classes",
        store=True,
        string="Tags' CSS Classes",
        help="Technical field for concatenating all tags' CSS classes",
    )

    @api.depends("tag_ids", "tag_ids.css_classes")
    def _compute_css_classes(self):
        for blog_post in self:
            blog_post.tags_css_classes = " ".join(
                tag.css_classes.strip() for tag in blog_post.tag_ids if tag.css_classes
            )
