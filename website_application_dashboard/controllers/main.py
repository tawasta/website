##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2023- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import logging

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class ApplicationDashboardController(http.Controller):
    @http.route(
        [
            "/dashboard",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def dashboard(self, **post):
        """
        Render dashboard page


        {
            <category_id>: [app_user, ...],
            <category_id>: [app_user, ...],
        }
        """
        categories = request.env["dashboard.app.category"].search([])
        apps = request.env["dashboard.app.user"].get_user_apps(request.env.user.id)
        category_data = {}
        for categ in categories:
            category_data[categ.id] = apps.filtered(
                lambda r: r.application_id.category_id.id == categ.id
            )

        render_values = {
            "no_breadcrumbs": True,
            "categories": categories,
            "category_data": category_data,
        }
        return request.render(
            "website_application_dashboard.application_dashboard",
            render_values,
        )

    @http.route(
        [
            "/dashboard/save",
        ],
        type="json",
        auth="user",
    )
    def dashboard_save(self, **post):
        """Save dashboard page - positions and visibility"""
        for app_id in post.get("data"):
            sequence = post.get("data").get(app_id).get("position")
            hidden = post.get("data").get(app_id).get("hidden")
            data = request.env["dashboard.app.user"].browse(int(app_id))
            data.write(
                {
                    "sequence": sequence,
                    "visible": not hidden,
                }
            )
            data.sequence = sequence

    @http.route(
        [
            "/dashboard/create",
        ],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def dashboard_create(self, **post):
        """Create new application"""
        if post:
            name = post.get("name")
            url = post.get("url")
            categ_id = request.env.ref(
                "website_application_dashboard.dashboard_app_category_personal"
            ).id
            request.env["dashboard.app"].sudo().create(
                {
                    "name": name,
                    "url": url,
                    "user_id": request.env.uid,
                    "category_id": categ_id,
                }
            )
        return request.redirect("/dashboard")
