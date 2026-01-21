import logging

import werkzeug

from odoo import _, http
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError

_logger = logging.getLogger(__name__)


class AuthSignupHomeCustom(AuthSignupHome):
    @http.route("/web/signup", type="http", auth="user", website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        """Modification to original web_auth_signup method to disable creating
        users even when 'Free sign up' option is selected in website settings."""
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get("token") and not qcontext.get("signup_enabled"):
            raise werkzeug.exceptions.NotFound()

        if "error" not in qcontext and request.httprequest.method == "POST":
            try:
                if not request.env["ir.http"]._verify_request_recaptcha_token("signup"):
                    raise UserError(
                        _("Suspicious activity detected by Google reCaptcha.")
                    )

                self.do_signup(qcontext)

                # Set user to public if they were not signed in by do_signup
                # (mfa enabled)
                if request.session.uid is None:
                    public_user = request.env.ref("base.public_user")
                    request.update_env(user=public_user)

                # Send an account creation confirmation email
                User = request.env["res.users"]
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get("login")),
                    order=User._get_login_order(),
                    limit=1,
                )
                template = request.env.ref(
                    "auth_signup.mail_template_user_signup_account_created",
                    raise_if_not_found=False,
                )
                if user_sudo and template:
                    template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext["error"] = e.args[0]
            except (SignupError, AssertionError) as e:
                if (
                    request.env["res.users"]
                    .sudo()
                    .search([("login", "=", qcontext.get("login"))])
                ):
                    qcontext["error"] = _(
                        "Another user is already registered using this email address."
                    )
                else:
                    _logger.warning("%s", e)
                    qcontext["error"] = (
                        _("Could not create a new account.") + "\n" + str(e)
                    )

        response = request.render("auth_signup.signup", qcontext)
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Content-Security-Policy"] = "frame-ancestors 'self'"
        return response
