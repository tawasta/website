from odoo import models, fields, _


class ResCountry(models.Model):
    _inherit = "res.country"

    website_published = fields.Boolean(
        string="Show in Website Country Selection",
        help=_(
            """Adds this country to selectable countries on eCommerce and
                  My Account"""
        ),
        default=False,
    )
