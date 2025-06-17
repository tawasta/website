import logging

from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class WebsiteEditorRightsWebsiteSpecific(Website):
    @http.route()
    def client_action_redirect(self, path="", **kw):
        # Raise an access error when trying to launch the editor from frontend
        # top left icon

        if request.website.sudo().allowed_editor_group_id:
            if (
                request.website.sudo().allowed_editor_group_id
                not in request.env.user.groups_id
            ):
                raise AccessError(
                    _("You do not have permissions edit website %s.")
                    % request.website.name
                )

        return super().client_action_redirect(path, **kw)
