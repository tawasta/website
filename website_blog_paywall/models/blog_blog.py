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

    partner_domain_filter_ids = fields.Many2many(
        "partner.domain.filter",
        "blog_domain_filter_rel",
        string="Paywall criteria",
    )

    partner_free_domain_filter_ids = fields.Many2many(
        "partner.domain.filter",
        "blog_free_domain_filter_rel",
        string="Paywall free tier criteria",
    )
