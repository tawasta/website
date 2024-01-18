from odoo import fields, models


class SlideSlide(models.Model):

    _inherit = "slide.slide"

    slide_type = fields.Selection(selection_add=[("infographic", "Image")])
