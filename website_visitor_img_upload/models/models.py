from odoo import models, fields, api
import datetime

class WebsiteVisitorImage(models.Model):
    _name = 'visitor.image'
    _description = 'Image uploaded by website visitor'

    name = fields.Char(string="Name")
    date = fields.Date(string='Date')
    website_published = fields.Boolean(string="Published on website", default=False)
    image = fields.Binary('Image', attachment=True)

    @api.model
    def get_published(self):
        images = self.search([('website_published', '=', True)]).id
        return images

    @api.model
    def create(self, vals):
        vals['date'] = datetime.datetime.now()
        vals['name'] = "Visitor Image"
        super(WebsiteVisitorImage, self).create(vals)

