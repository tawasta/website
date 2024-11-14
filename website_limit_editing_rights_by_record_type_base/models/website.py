from odoo import models, _
from odoo.exceptions import AccessError, AccessDenied

import logging

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    def _get_models_allowed_to_be_edited(self):
        # Inherit in separate modules to add "event.event", "slide.channel" etc. strings.
        # Editing is categorigally denied for any models not listed in the array.
        # This prevents write access to e.g. generic website pages and products.
        return []

    def _check_record_access(self, record_model, record_id):
        # If the user has write access to the record, they are also allowed to edit
        # the page.

        object_being_edited = self.env[record_model].search(
            [("id", "=", record_id)], limit=1
        )

        try:
            object_being_edited.check_access_rule("write")
        except AccessError:
            # Raise a less detailed error than the default
            raise AccessDenied(
                _(
                    "You don't have permissions to edit this record in the website editor."
                )
            )

        return

    def _check_model_access(self, record_model):
        # Check which models' related pages are allowed to be edited

        allowed_models = self._get_models_allowed_to_be_edited()

        if record_model not in allowed_models:
            raise AccessDenied(
                _(
                    "You don't have permissions to edit this type of content in the website editor."
                )
            )

    def check_limited_website_editor_access(self, record_model, record_id):
        # Access rights check function called from JS when editor is launched.
        if self.env.user.has_group(
            "website_limit_editing_rights_by_record_type_base.group_website_limit_editing_rights_by_record_type_base"
        ):
            self._check_model_access(record_model)
            self._check_record_access(record_model, record_id)

        return self._get_models_allowed_to_be_edited()
