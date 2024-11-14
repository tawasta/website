from odoo import models, _
from odoo.exceptions import AccessDenied


class Website(models.Model):
    _inherit = "website"

    def _get_models_allowed_to_be_edited(self):
        # Grant access to edit channels and slides in website builder

        res = super()._get_models_allowed_to_be_edited()

        if self.env.user.has_group(
            "website_limit_editing_rights_by_record_type_elearning.group_website_limit_editing_rights_by_record_type_elearning"
        ):
            res.append("slide.channel")
            res.append("slide.slide")

        return res
