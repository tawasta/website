from odoo import fields, models


class Blog(models.Model):
    _inherit = "blog.blog"

    paywall = fields.Boolean(
        "Paid articles",
        help="Require a permission for reading posts in this blog",
        default=False,
    )

    paywall_description = fields.Html(
        "Paywall description",
        translate=True,
        help="Tell your readers why this blog is behind a paywall",
    )

    paywall_domain = fields.Char(
        string="Paywall criteria",
    )
