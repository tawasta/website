import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Slide(models.Model):

    _inherit = "slide.slide"

    image_uncompressed = fields.Binary(
        string="Image (uncompressed original)", attachment=True
    )

    def _unoptimized_images_enabled(self):
        """
        Check config params if unoptimized image should be stored
        """

        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_slides.store_uncompressed_images")
        )

    @api.model
    def create(self, values):
        """
        Pass a context parameter to core's ir_attachment._postprocess_contents()
        function so that it skips compressing and resizing of images.

        Note: This does not affect the image_1920, image_1024 fields, but would affect
        if the slide had other binary fields with image contents, i.e. those would
        not get compressed/resized either.
        """

        uploaded_from_website = self.env.context.get("website_id")

        if self._unoptimized_images_enabled():
            # This is needed so that upload works from both backend and from website.
            # In backend the image_uncompressed value is already present and should not
            # be copied from datas, as datas may contain an empty value, depending
            # on slide_type.

            if uploaded_from_website and values.get("datas"):
                values["image_uncompressed"] = values["datas"]

            self = self.with_context(image_no_postprocess=True)

        return super(Slide, self).create(values)

    def write(self, values):
        """
        Also in write(), pass a context parameter to core's
        ir_attachment._postprocess_contents() function so that it skips compressing
        and resizing of images.
        """
        if self._unoptimized_images_enabled():
            self = self.with_context(image_no_postprocess=True)

        return super(Slide, self).write(values)

    @api.onchange("datas")
    def _on_change_datas(self):
        """
        If adding/editing the slide via backend, core's on_change_datas() moves the
        uploaded  image from 'datas' to 'image_1920' and then clears 'datas' field
        altogether,  so we need to grab the image data before that happens.
        """

        if self.datas and self._unoptimized_images_enabled():
            self.image_uncompressed = self.datas

        return super()._on_change_datas()
