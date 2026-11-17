import json

from odoo import _, http
from odoo.exceptions import AccessDenied
from odoo.http import request
from odoo.tools.mail import single_email_re


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
            # The login is written with sudo, so internal users must not be
            # able to bypass the admin-only login change through this route
            if not user._is_portal():
                response.update(
                    {
                        "error": True,
                        "msg": _("Only portal users can change their username here."),
                    }
                )
                return json.dumps(response)

            # Checked before any lookup so that a hijacked session cannot
            # change the credential or probe existing logins
            if not self._is_password_valid(post.get("password", "")):
                response.update({"error": True, "msg": _("Wrong password.")})
                return json.dumps(response)

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

            sync_partner_email = self._is_partner_email_sync_enabled()
            if sync_partner_email and not single_email_re.match(new_login):
                response.update(
                    {
                        "error": True,
                        "msg": _("The new username must be a valid email address."),
                    }
                )
                return json.dumps(response)

            old_login = user.login
            values = {"login": new_login}
            if sync_partner_email:
                # Written through the user so that core sends the security
                # notice to the previous address and tracks the partner email
                values["email"] = new_login
            # The error response below must not leave a committed login change
            # behind if the chatter note fails
            with request.env.cr.savepoint():
                user.sudo().write(values)
                self._log_username_change(user, old_login, new_login)
            request.session.logout()

        except Exception:
            response.update(
                {
                    "error": True,
                    "msg": _("An error occurred while changing the username."),
                }
            )

        return json.dumps(response)

    def _is_password_valid(self, password):
        # Same check as core uses before deactivating a portal account
        if not password:
            return False
        try:
            request.env["res.users"]._check_credentials(password, {"interactive": True})
        except AccessDenied:
            return False
        return True

    def _is_partner_email_sync_enabled(self):
        # sudo: portal users cannot read system parameters
        return bool(
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("website_portal_username_change.sync_partner_email")
        )

    def _log_username_change(self, user, old_login, new_login):
        # sudo: message_post requires write access, which a portal user does
        # not have on their own partner; the author stays the portal user
        user.partner_id.sudo().message_post(
            body=_(
                "Username changed from %(old_login)s to %(new_login)s via the portal.",
                old_login=old_login,
                new_login=new_login,
            ),
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )

    @http.route(["/my/change_username/modal"], type="json", auth="user", website=True)
    def get_change_username_modal(self):
        user = request.env.user
        return request.env["ir.ui.view"]._render_template(
            "website_portal_username_change.change_username_modal",
            {"current_login": user.login},
        )
