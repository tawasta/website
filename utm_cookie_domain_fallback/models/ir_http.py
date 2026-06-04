# -*- coding: utf-8 -*-

import logging

from odoo import models
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _set_utm(cls, response):
        """
        Odoo 17 core sets UTM cookies with domain=request.httprequest.host.

        Some runtime host values are not valid cookie domains. This can happen
        behind reverse proxies, with ports, internal hostnames, local/dev hosts,
        or otherwise invalid Host headers. Werkzeug raises ValueError and Odoo
        returns 500 for URLs containing utm_source / utm_medium / utm_campaign.

        Keep Odoo's original behavior first. If setting the cookie with the
        original domain fails, retry without explicit domain. That creates a
        valid host-only cookie and prevents the page request from crashing.
        """
        response = Response.load(response)
        domain = cls.get_utm_domain_cookies()

        for url_parameter, __, cookie_name in request.env["utm.mixin"].tracking_fields():
            if (
                url_parameter in request.params
                and request.httprequest.cookies.get(cookie_name) != request.params[url_parameter]
            ):
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
                        "Invalid UTM cookie domain %r for host %r while setting %r. "
                        "Retrying without explicit domain. Error: %s",
                        domain,
                        request.httprequest.host,
                        cookie_name,
                        error,
                    )
                    response.set_cookie(
                        cookie_name,
                        request.params[url_parameter],
                        max_age=31 * 24 * 3600,
                        cookie_type="optional",
                    )