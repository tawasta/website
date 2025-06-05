from odoo import http
from odoo.http import request


class WebsiteCreateCompany(http.Controller):
    @http.route("/company/create/submit", type="http", auth="public", website=True)
    def company_create_submit(self, **post):
        # Create a new company

        name = post.get("name")
        company_registry = post.get("company_registry")

        request.env["res.partner"].sudo().create(
            {
                "name": name,
                "company_registry": company_registry,
            }
        )

        return request.render("website_create_company.company_create_success")

    @http.route("/company/create", type="http", auth="public", website=True)
    def company_create(self, **kw):
        return request.render("website_create_company.company_create")
