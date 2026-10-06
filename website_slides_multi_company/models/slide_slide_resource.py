from odoo import fields, models


class SlideSlideResource(models.Model):
    _inherit = "slide.slide.resource"

    company_id = fields.Many2one(
        "res.company",
        related="slide_id.company_id",
        store=True,
        index=True,
    )
