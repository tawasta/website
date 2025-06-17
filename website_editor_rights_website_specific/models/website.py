import logging

from odoo import _, fields, models
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    allowed_editor_group_id = fields.Many2one(
        string="Required Group Membership for Editing",
        comodel_name="res.groups",
        help="If set, to edit this website the user needs to be also in this group, "
        "in addition to the standard Website Editor or Website Restricted "
        "Editor group.",
    )

    def get_client_action(self, url, mode_edit=False, website_id=False):
        # Removes the editor bar when clicking the "Go to website" buttons in backend

        res = super().get_client_action(
            url=url, mode_edit=mode_edit, website_id=website_id
        )

        if website_id:
            website_sudo = self.env["website"].sudo().search([("id", "=", website_id)])

            if website_sudo.allowed_editor_group_id:
                if website_sudo.allowed_editor_group_id not in self.env.user.groups_id:
                    return {"type": "ir.actions.act_url", "url": url}

        return res

    def check_website_specific_editor_access(self):
        # Access rights check function called from JS when editor is launched.
        if self.allowed_editor_group_id:
            if self.allowed_editor_group_id not in self.env.user.groups_id:
                raise AccessDenied(
                    _("You do not have permissions edit website %s.") % self.name
                )
