# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import request

from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlidesTagBasedSearch(WebsiteSlides):
    def _prepare_additional_channel_values(self, values, **kwargs):
        """
        Fetch all the slide tags
        """

        values = super(
            WebsiteSlidesTagBasedSearch, self
        )._prepare_additional_channel_values(values, **kwargs)

        fields = ["id", "name"]
        order = "name ASC"

        values["slide_tags"] = request.env["slide.tag"].search_read(
            fields=fields, order=order
        )

        return values
