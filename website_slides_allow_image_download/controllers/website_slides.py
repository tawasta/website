from odoo.http import request

from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlidesAllowImageDownload(WebsiteSlides):
    def _prepare_additional_channel_values(self, values, **kwargs):
        """
        Add info about if image download button should be shown
        """

        values = super(
            WebsiteSlidesAllowImageDownload, self
        )._prepare_additional_channel_values(values, **kwargs)

        ir_config = request.env["ir.config_parameter"]

        # Button shown if config and slide type allow
        values["show_image_download_button"] = (
            ir_config.sudo().get_param("website_slides.show_download_link_for_images")
            and values.get("slide")
            and values["slide"].slide_type == "infographic"
        )

        return values
