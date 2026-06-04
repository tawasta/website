import logging

from odoo import models
from odoo.http import Response, request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _set_utm(cls, response):
        """
        Temporary debug version for investigating invalid UTM cookie domains.
        """

        response = Response.load(response)
        domain = cls.get_utm_domain_cookies()

        _logger.warning(
            "UTM DEBUG START: "
            "domain=%r host=%r http_host=%r server_name=%r server_port=%r "
            "url=%r x_forwarded_host=%r x_forwarded_proto=%r",
            domain,
            request.httprequest.host,
            request.httprequest.environ.get("HTTP_HOST"),
            request.httprequest.environ.get("SERVER_NAME"),
            request.httprequest.environ.get("SERVER_PORT"),
            request.httprequest.url,
            request.httprequest.headers.get("X-Forwarded-Host"),
            request.httprequest.headers.get("X-Forwarded-Proto"),
        )

        for url_parameter, __, cookie_name in request.env[
            "utm.mixin"
        ].tracking_fields():
            if (
                url_parameter in request.params
                and request.httprequest.cookies.get(cookie_name)
                != request.params[url_parameter]
            ):
                _logger.warning(
                    "UTM DEBUG COOKIE: "
                    "cookie_name=%r url_parameter=%r value=%r "
                    "domain=%r host=%r http_host=%r",
                    cookie_name,
                    url_parameter,
                    request.params[url_parameter],
                    domain,
                    request.httprequest.host,
                    request.httprequest.environ.get("HTTP_HOST"),
                )

                try:
                    response.set_cookie(
                        cookie_name,
                        request.params[url_parameter],
                        max_age=31 * 24 * 3600,
                        domain=domain,
                        cookie_type="optional",
                    )

                except ValueError as error:
                    _logger.warning(
                        "UTM DEBUG COOKIE FAILED: "
                        "cookie_name=%r domain=%r host=%r http_host=%r "
                        "server_name=%r server_port=%r error=%s",
                        cookie_name,
                        domain,
                        request.httprequest.host,
                        request.httprequest.environ.get("HTTP_HOST"),
                        request.httprequest.environ.get("SERVER_NAME"),
                        request.httprequest.environ.get("SERVER_PORT"),
                        error,
                    )

                    response.set_cookie(
                        cookie_name,
                        request.params[url_parameter],
                        max_age=31 * 24 * 3600,
                        cookie_type="optional",
                    )

                    _logger.warning(
                        "UTM DEBUG COOKIE FALLBACK OK: " "cookie_name=%r",
                        cookie_name,
                    )
