from odoo import fields, models


class SlideSlide(models.Model):
    _inherit = "slide.slide"

    company_id = fields.Many2one(
        "res.company",
        related="channel_id.company_id",
        store=True,
        index=True,
    )


class SlideSlidePartner(models.Model):
    _inherit = "slide.slide.partner"

    company_id = fields.Many2one(
        "res.company",
        related="channel_id.company_id",
        store=True,
        index=True,
    )
