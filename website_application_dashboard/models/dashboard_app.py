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
import sys
import timeit
import traceback

import requests

# 3. Odoo imports (openerp):
from odoo import _, fields, models
from odoo.exceptions import UserError

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class DashboardApp(models.Model):

    # 1. Private attributes
    _name = "dashboard.app"
    _description = "Dashboard Application"
    _rec_name = "name"
    _sql_constraints = [
        (
            "dashboard_application_api_id_uniq",
            "unique (application_api_id)",
            _("Application API ID already exists!"),
        )
    ]

    # 2. Fields declaration
    name = fields.Char(
        help="Name of the application",
        required=True,
    )
    info = fields.Html(
        help="Info for the application",
        translate=True,
        sanitize=False,
    )
    description = fields.Text(
        help="Description for the application",
    )
    url = fields.Char(
        help="URL for the application",
        required=True,
    )
    app_user_ids = fields.One2many(
        comodel_name="dashboard.app.user",
        inverse_name="application_id",
        string="Application user datas",
        help="User datas related to this application",
    )
    application_api_id = fields.Integer(
        string="API ID",
        help="Application ID in API",
    )
    category_id = fields.Many2one(
        comodel_name="dashboard.app.category",
        string="Category",
        help="To what category this application belongs to",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Created user",
        help="User created this personal dashboard application",
    )
    # TODO: Do we need border color as well? Or use predefined classnames with
    # ready made styles (3-5 pcs)?
    color = fields.Char(
        string="Color code",
        help="Color code for cards styling",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_applications(self):
        """Get applications from API"""
        try:
            endpoint_url = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("website_application_dashboard.app_endpoint", "")
            )
            api_key = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("website_application_dashboard.api_key", "")
            )
            if not (endpoint_url and api_key):
                _logger.error("Endpoint or API key missing")
                raise Exception

            # Create headers and send request
            headers = {
                "Authorization": "Bearer {}".format(api_key),
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            res = requests.get(endpoint_url, headers=headers, timeout=10)
            _logger.info("Response status code {}".format(res.status_code))
            if res.ok:
                data = res.json()
                _logger.info(
                    "Received {} applications, create missing ones".format(len(data))
                )
                current_applications = self.search(
                    [
                        ("user_id", "=", False),
                    ]
                ).mapped("application_api_id")
                new_apps = []
                for app in data:
                    if app.get("application_id") not in current_applications:
                        # Find category with ID
                        category_id = app.pop("category_id")
                        category = self.env["dashboard.app.category"].search(
                            [("category_api_id", "=", category_id)], limit=1
                        )
                        if not category:
                            _logger.error(
                                "No category found with {}".format(category_id)
                            )
                            raise Exception

                        app["application_api_id"] = app.pop("application_id")
                        app["category_id"] = category.id
                        new_apps.append(app)

                if new_apps:
                    _logger.info("Creating {} new applications".format(len(new_apps)))
                    self.create(new_apps)

        except Exception:
            msg = _("Error occured when fetching application data")
            _logger.error(msg)
            info = sys.exc_info()
            formatted_info = "".join(traceback.format_exception(*info))
            _logger.error(formatted_info)
            raise UserError(msg) from None

    def action_cron_update_applications(self):
        """Cron to update user data from API"""
        _logger.info("Dashboard cron: Update applications...")
        start = timeit.default_timer()
        try:
            self._get_applications()
        except Exception:
            # Send to mattermost
            pass
            # hook = (
            #     self.env["mattermost.hook"]
            #     .sudo()
            #     .search(
            #         [
            #             ("res_model", "=", "dashboard.app.user"),
            #             ("function", "=", "get_user_app_data"),
            #             ("hook", "!=", False),
            #         ],
            #         limit=1,
            #     )
            # )
            # if hook:
            #     msg = (
            #         "### :school: Dashboard data"
            #         "\n Failed to fetch dashboard data!"
            #     ).format(len(self))
            #     hook.post_mattermost(msg)
            raise
        exec_time = timeit.default_timer() - start
        _logger.info(
            "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
        )

    # 8. Business methods
