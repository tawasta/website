from odoo import fields, models


class Blog(models.Model):
    _inherit = "blog.blog"

    paywall = fields.Boolean(
        "Paid articles",
        help="Require a permission for reading posts in this blog",
        default=False,
    )

    paywall_free_articles = fields.Integer(
        "Free articles",
        help="Allows a free tier for paid articles",
        default=0,
    )

    paywall_description = fields.Html(
        "Paywall description",
        translate=True,
        help="Tell your readers why this blog is behind a paywall",
    )

    paywall_teaser_length = fields.Integer(
        "Teaser length",
        default=200,
    )

    paywall_domain = fields.Char(
        string="Paywall criteria",
    )

    paywall_free_domain = fields.Char(
        string="Paywall free tier criteria",
    )
