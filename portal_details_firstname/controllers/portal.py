from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalDetails(CustomerPortal):
    # Required fields are defined in a list MANDATORY_BILLING_FIELDS
    CustomerPortal.MANDATORY_BILLING_FIELDS.extend(["firstname", "lastname"])

    @http.route()
    def account(self, redirect=None, **post):
        if post and request.httprequest.method == "POST" and post.get("firstname"):
            post["name"] = request.env["res.partner"]._get_computed_name(
                post.get("lastname"), post.get("firstname")
            )
        return super().account(redirect=redirect, **post)
