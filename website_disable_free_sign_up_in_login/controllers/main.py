from odoo import http

from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class AuthSignupHomeCustom(AuthSignupHome):
    # Only the route's auth is changed; the other route arguments
    # (captcha, website, sitemap) are merged from the overridden route.
    @http.route(auth="user")
    def web_auth_signup(self, *args, **kw):
        """Require a logged-in user so that accounts cannot be created from
        the login screen even when 'Free sign up' is enabled."""
        return super().web_auth_signup(*args, **kw)
