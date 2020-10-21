from odoo import fields
from odoo import models


class Slide(models.Model):

    _inherit = "slide.slide"

    website_description = fields.Html("Website description")
