from odoo import models, _
from odoo.exceptions import AccessDenied


class Website(models.Model):
    _inherit = "website"

    def _get_models_allowed_to_be_edited(self):
        res = super()._get_models_allowed_to_be_edited()

        if self.env.user.has_group(
            "website_limit_editing_rights_by_record_type_event.group_website_limit_editing_rights_by_record_type_event"
        ):
            res.append("event.event")

        return res
