from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    slides_banner_image = fields.Image(
        readonly=False,
        store=True,
        max_width=1920,
        max_height=1080,
        verify_resolution=True,
    )
