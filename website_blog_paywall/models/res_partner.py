from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

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
