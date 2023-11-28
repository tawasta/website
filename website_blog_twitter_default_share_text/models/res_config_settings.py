from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    twitter_default_blog_post_share_text = fields.Char(
        string="Twitter default Blog Post share text",
        related="website_id.twitter_default_blog_post_share_text",
        readonly=False,
        help="Text to be suggested as default, when sharing a blog post to Twitter. "
        "The first placeholder contains the blog post title. The second placeholder "
        "contains the URL.",
    )
