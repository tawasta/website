import base64
import logging

from odoo import http
from odoo.http import content_disposition, request
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)


class SlideDownloadController(http.Controller):
    @http.route(
        '/slides/slide/<model("slide.slide"):slide>/download_image', auth="public"
    )
    def download_slide(self, slide, **kwargs):

        ir_config = request.env["ir.config_parameter"]

        # If wrong slide type, or config option not enabled, don't allow downloading
        if not slide.slide_type == "infographic" or not ir_config.sudo().get_param(
            "website_slides.show_download_link_for_images"
        ):
            return request.render("website.page_404")

        # If uncompressed image is available, use that, but fall back to core's
        if slide.image_uncompressed:
            image_source = slide.image_uncompressed
            _logger.debug("Downloading original high-res image for slide %s", slide.id)
        else:
            image_source = slide.datas
            _logger.debug("Downloading compressed image for slide %s", slide.id)

        # If for some reason nothing found in either, log an error
        if not image_source:
            _logger.error(
                "Could not find image data for slide ID %s via download link", slide.id
            )
            return request.render("website.page_404")

        data = base64.b64decode(image_source)

        # Extract mimetype directly from the data, since it seems that the
        # slide.mime_type field is sometimes not filled in automatically
        mime_type = guess_mimetype(data)
        filename = "{}.{}".format(
            slide.name, "jpg" if mime_type == "image/jpeg" else "png"
        )

        return request.make_response(
            data,
            [
                ("Content-Type", mime_type),
                ("Content-Disposition", content_disposition(filename)),
            ],
        )
