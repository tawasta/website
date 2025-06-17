import logging

import werkzeug.urls

from odoo import models

_logger = logging.getLogger(__name__)

try:
    from odoo.http import request
except ImportError:
    request = None


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _compute_signup_url(self):
        # Call the original Odoo implementation first
        super()._compute_signup_url()

        # Now apply custom logic if request context is available
        if not request:
            return

        referer = request.httprequest.headers.get("Referer", "")
        request_path = request.httprequest.path

        for partner in self:
            signup_url = partner.signup_url
            if (
                signup_url
                and request_path
                and "/reset_password" in request_path
                and "/reset_password" in signup_url
                and referer
            ):
                parsed_referer = werkzeug.urls.url_parse(referer)
                parsed_signup = werkzeug.urls.url_parse(signup_url)

                # Tarkistetaan, ovatko domainit eriäviä
                if parsed_signup.host != parsed_referer.host:
                    # Korvataan domain signup_url:ssä refererin domainilla
                    new_signup_url = parsed_signup.replace(
                        netloc=parsed_referer.netloc
                    ).to_url()
                    partner.signup_url = new_signup_url
