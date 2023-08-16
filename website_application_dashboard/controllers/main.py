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
        """Render dashboard page"""
        apps = request.env["dashboard.app"].sudo().search([])
        render_values = {
            "no_breadcrumbs": True,
            "apps": apps,
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
        """Save dashboard page"""
        _logger.info(post)
        return request.redirect("/dashboard")
