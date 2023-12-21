from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Website(models.Model):

    _inherit = "website"

    twitter_default_blog_post_share_text = fields.Char(
        string="Twitter default Blog Post share text",
        store=True,
        help="Text to be suggested as default, when sharing a blog post to Twitter. "
        "The first placeholder contains the blog post title. The second placeholder "
        "contains the URL.",
    )

    @api.constrains("twitter_default_blog_post_share_text")
    def _check_twitter_default_blog_post_share_text(self):
        for record in self:
            if record.twitter_default_blog_post_share_text.count("%s") != 2:
                raise ValidationError(
                    _(
                        "The string must contain two '%s' placeholders. First one "
                        "will contain the title of the blog post, the second one "
                        "will contain the URL."
                    )
                )
