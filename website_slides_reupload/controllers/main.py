import werkzeug
from odoo import http, _
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlidesExtended(WebsiteSlides):
    def _get_slide_detail(self, slide):
        res = super()._get_slide_detail(slide)

        download_only = (
            slide.slide_type == "document" and slide.mime_type != "application/pdf"
        )
        res["download_only"] = download_only

        return res
