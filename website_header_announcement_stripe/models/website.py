from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    header_announcement_stripe_show = fields.Boolean(
        "Show Header Announcement Stripe", readonly=False
    )
    header_announcement_stripe_text = fields.Html(readonly=False, translate=True)
