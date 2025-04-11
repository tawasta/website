from odoo import models, fields, api
from datetime import datetime
import random


class AdvertisementCategory(models.Model):
    _name = "advertisement.category"
    _description = "Advertisement Category"

    name = fields.Char(required=True)
    description = fields.Text()


class Advertisement(models.Model):
    _name = "advertisement.advertisement"
    _description = "Advertisement"

    name = fields.Char(required=True)
    advertisement_category_ids = fields.Many2many(
        "advertisement.category", string="Categories"
    )

    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True)
    image = fields.Binary()
    url = fields.Char()
    is_active = fields.Boolean(default=True)
    view_count = fields.Integer(default=0)
    click_count = fields.Integer(default=0)

    image_url = fields.Char(compute="_compute_image_url", readonly=True)

    # Computed image URL for use in frontend
    @api.depends("image")
    def _compute_image_url(self):
        for record in self:
            if record.image:
                record.image_url = f"/web/image/{record._name}/{record.id}/image"
            else:
                record.image_url = "/web/static/img/placeholder.png"

    def increment_view(self):
        self.sudo().write({"view_count": self.view_count + 1})

    def increment_click(self):
        self.sudo().write({"click_count": self.click_count + 1})

    # Used by snippet rendering to get image and fallback
    @property
    def cover_properties(self):
        return {
            "image_field": "image",
            "default_image": "/web/static/img/placeholder.png",
        }
