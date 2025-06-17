from odoo import models
import logging
import werkzeug.urls

_logger = logging.getLogger(__name__)

try:
    from odoo.http import request
except ImportError:
    request = None  # Ei HTTP-kontekstia

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _compute_signup_url(self):
        result = self.sudo()._get_signup_url_for_action()

        referer = None
        request_path = None

        if request:
            referer = request.httprequest.headers.get('Referer', '')
            request_path = request.httprequest.path
            _logger.info("Signup URL computed from HTTP path: %s, referer: %s", request_path, referer)
        else:
            _logger.info("Signup URL computed outside HTTP context")

        for partner in self:
            if any(u._is_internal() for u in partner.user_ids if u != self.env.user):
                self.env['res.users'].check_access_rights('write')
            if any(u.has_group('base.group_portal') for u in partner.user_ids if u != self.env.user):
                self.env['res.partner'].check_access_rights('write')

            signup_url = result.get(partner.id, False)

            if signup_url and request_path and '/reset_password' in request_path and '/reset_password' in signup_url and referer:
                parsed_referer = werkzeug.urls.url_parse(referer)
                parsed_signup = werkzeug.urls.url_parse(signup_url)

                # Tarkista että domainit eroavat
                if parsed_signup.host != parsed_referer.host:
                    # Korvaa domain signup_urlissa refererillä
                    new_signup_url = parsed_signup.replace(netloc=parsed_referer.netloc).to_url()
                    _logger.info("Overriding domain in signup URL due to referer mismatch: %s -> %s", signup_url, new_signup_url)
                    signup_url = new_signup_url

            _logger.info("Generated signup URL for partner [%s - %s]: %s", partner.id, partner.name, signup_url)
            partner.signup_url = signup_url
