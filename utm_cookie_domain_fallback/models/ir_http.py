import logging

from odoo import models
from odoo.http import Response, request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _set_utm(cls, response):
        """
        Temporary debug-only override for Odoo 17 UTM cookie handling.

        This intentionally keeps the same behavior as Odoo core:
        - uses cls.get_utm_domain_cookies()
        - calls response.set_cookie(..., domain=domain)
        - does NOT retry without domain
        - does NOT fix the request

        Purpose: log the exact request/WSGI/proxy/cookie-domain values before
        Odoo/Werkzeug raises the original error.
        """
        response = Response.load(response)
        domain = cls.get_utm_domain_cookies()
        environ = request.httprequest.environ
        headers = request.httprequest.headers

        _logger.warning(
            "UTM DEBUG START: "
            "domain=%r host=%r http_host=%r server_name=%r server_port=%r "
            "scheme=%r url=%r path=%r query=%r "
            "x_forwarded_host=%r x_forwarded_proto=%r x_forwarded_for=%r "
            "x_real_ip=%r forwarded=%r",
            domain,
            request.httprequest.host,
            environ.get("HTTP_HOST"),
            environ.get("SERVER_NAME"),
            environ.get("SERVER_PORT"),
            request.httprequest.scheme,
            request.httprequest.url,
            request.httprequest.path,
            request.httprequest.query_string.decode("utf-8", errors="replace"),
            headers.get("X-Forwarded-Host"),
            headers.get("X-Forwarded-Proto"),
            headers.get("X-Forwarded-For"),
            headers.get("X-Real-IP"),
            headers.get("Forwarded"),
        )

        for url_parameter, __, cookie_name in request.env[
            "utm.mixin"
        ].tracking_fields():
            current_cookie_value = request.httprequest.cookies.get(cookie_name)
            param_value = request.params.get(url_parameter)

            _logger.warning(
                "UTM DEBUG FIELD CHECK: "
                "url_parameter=%r cookie_name=%r param_present=%r "
                "param_value=%r current_cookie_value=%r will_set_cookie=%r",
                url_parameter,
                cookie_name,
                url_parameter in request.params,
                param_value,
                current_cookie_value,
                url_parameter in request.params and current_cookie_value != param_value,
            )

            if (
                url_parameter in request.params
                and current_cookie_value != request.params[url_parameter]
            ):
                _logger.warning(
                    "UTM DEBUG SET_COOKIE CORE CALL: "
                    "cookie_name=%r url_parameter=%r value=%r domain=%r "
                    "host=%r http_host=%r server_name=%r server_port=%r",
                    cookie_name,
                    url_parameter,
                    request.params[url_parameter],
                    domain,
                    request.httprequest.host,
                    environ.get("HTTP_HOST"),
                    environ.get("SERVER_NAME"),
                    environ.get("SERVER_PORT"),
                )

                # Same as Odoo core. No fallback here.
                response.set_cookie(
                    cookie_name,
                    request.params[url_parameter],
                    max_age=31 * 24 * 3600,
                    domain=domain,
                    cookie_type="optional",
                )
