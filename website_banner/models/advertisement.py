from odoo import models, fields, api
from datetime import datetime
import random

class AdvertisementCategory(models.Model):
    _name = 'advertisement.category'
    _description = 'Advertisement Category'

    name = fields.Char(required=True)
    description = fields.Text()


class Advertisement(models.Model):
    _name = 'advertisement.advertisement'
    _description = 'Advertisement'

    name = fields.Char(required=True)
    advertisement_category_id = fields.Many2one('advertisement.category', required=True)
    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True)
    image = fields.Binary()
    url = fields.Char()
    is_active = fields.Boolean(default=True)
    view_count = fields.Integer(default=0)
    click_count = fields.Integer(default=0)

    @api.model
    def get_random_ad(self, category_id):
        now = datetime.now()
        ads = self.search([
            ('advertisement_category_id', '=', category_id),
            ('is_active', '=', True),
            ('start_date', '<=', now),
            ('end_date', '>=', now),
        ])
        return random.choice(ads) if ads else None

    def increment_view(self):
        self.sudo().write({'view_count': self.view_count + 1})

    def increment_click(self):
        self.sudo().write({'click_count': self.click_count + 1})
