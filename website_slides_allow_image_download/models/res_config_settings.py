from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    website_slides_store_uncompressed_images = fields.Boolean(
        string="Store also Uncompressed Versions of Images",
        config_parameter="website_slides.store_uncompressed_images",
        default=False,
    )

    website_slides_show_download_link_for_images = fields.Boolean(
        string="Show Download Link for Images",
        config_parameter="website_slides.show_download_link_for_images",
        default=False,
    )
