from odoo import models, fields, api

class WebsiteVisitorImage(models.Model):
    _name = 'visitor.image'
    _description = 'Image uploaded by website visitor'

    name = fields.Char(string="Name")
    website_published = fields.Boolean(string="Published on website", default=False)
    active = fields.Boolean(default=True)
    image_url = fields.Char(string="Image URL")
    filename = fields.Char(string="Filename")
    attachment = fields.Many2one(string="Attachment Image", comodel_name="ir.attachment")
    attachment_image = fields.Binary(related="attachment.datas")

    @api.model
    def get_published_urls(self):
        image_urls = []
        for image in self.search([('website_published', '=', True)]):
            image_urls.append(image.image_url)
        return image_urls

    @api.model
    def create(self, vals):
        super(WebsiteVisitorImage, self).create(vals)
