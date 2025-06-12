import json

from odoo import _, http
from odoo.http import request


class PortalUserController(http.Controller):
    @http.route(
        ["/my/change_username"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def change_username(self, **post):
        response = {
            "error": False,
            "success": _("Username changed successfully! You will be logged out."),
        }

        try:
            user = request.env.user
            new_login = post.get("new_login", "").strip()
            confirm_login = post.get("confirm_login", "").strip()

            if not new_login or not confirm_login:
                response.update(
                    {"error": True, "msg": _("New username cannot be empty.")}
                )
                return json.dumps(response)

            if new_login != confirm_login:
                response.update({"error": True, "msg": _("Usernames do not match.")})
                return json.dumps(response)

            existing_user = (
                request.env["res.users"]
                .sudo()
                .search([("login", "=", new_login)], limit=1)
            )
            if existing_user:
                response.update(
                    {"error": True, "msg": _("This username is already taken.")}
                )
                return json.dumps(response)

            user.sudo().write({"login": new_login})
            request.session.logout()

        except Exception:
            response.update(
                {
                    "error": True,
                    "msg": _("An error occurred while changing the username."),
                }
            )

        return json.dumps(response)

    @http.route(["/my/change_username/modal"], type="json", auth="user", website=True)
    def get_change_username_modal(self):
        user = request.env.user
        return request.env["ir.ui.view"]._render_template(
            "website_portal_username_change.change_username_modal",
            {"current_login": user.login},
        )
