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
        ondelete="cascade",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Created user",
        help="User created this personal dashboard application",
    )
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
            api_mode = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("website_application_dashboard.api_mode", "")
            )
            api_suffix = ""
            if api_mode == "test":
                api_suffix = "_test"

            endpoint_url = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param(
                    "website_application_dashboard.app_endpoint{}".format(api_suffix),
                    "",
                )
            )
            auth_header = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param(
                    "website_application_dashboard.auth_header{}".format(api_suffix), ""
                )
            )
            auth_header_value = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param(
                    "website_application_dashboard.auth_header_value{}".format(
                        api_suffix
                    ),
                    "",
                )
            )
            if not (endpoint_url and auth_header and auth_header_value):
                _logger.error("Endpoint or API key missing")
                raise Exception

            # Create headers and send request
            headers = {
                auth_header: auth_header_value,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            res = requests.get(endpoint_url, headers=headers, timeout=10)
            _logger.info("Response status code {}".format(res.status_code))
            if res.ok:
                data = res.json()
                if not isinstance(data, list) or len(data) == 0:
                    msg = _("API response is not a list or size is 0!")
                    raise UserError(msg)

                _logger.info(
                    "Received {} applications, create missing ones".format(len(data))
                )
                current = self.search(
                    [
                        ("user_id", "=", False),
                    ]
                )
                current_api_ids = current.mapped("application_api_id")
                new_recs = []
                handled = self.env["dashboard.app"]
                for rec_data in data:
                    category_id = rec_data.pop("category_id")
                    # Find category with ID
                    category = self.env["dashboard.app.category"].search(
                        [("category_api_id", "=", category_id)], limit=1
                    )
                    if not category:
                        _logger.error("No category found with {}".format(category_id))
                        continue

                    application_id = rec_data.pop("application_id")
                    if not application_id:
                        _logger.error(
                            "No application ID provided in payload {}".format(rec_data)
                        )
                        continue

                    rec_data["category_id"] = category.id

                    if application_id not in current_api_ids:
                        rec_data["application_api_id"] = application_id
                        new_recs.append(rec_data)
                    else:
                        # Update application info
                        rec = self.search(
                            [("application_api_id", "=", application_id)], limit=1
                        )
                        rec.write(rec_data)
                        handled |= rec

                if new_recs:
                    _logger.info("Creating {} new applications".format(len(new_recs)))
                    handled |= self.create(new_recs)

                removed_recs = current - handled
                if removed_recs:
                    _logger.info("Removing apps {}...".format(removed_recs))
                    removed_recs.unlink()

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
            _logger.error("Dashboard cron: sending error message to mattermost...")
            hook = (
                self.env["mattermost.hook"]
                .sudo()
                .search(
                    [
                        ("res_model", "=", "dashboard.app"),
                        ("function", "=", "_get_applications"),
                        ("hook", "!=", False),
                    ],
                    limit=1,
                )
            )
            if hook:
                msg = _(
                    "### :no_entry: Dashboard application data"
                    "\n Failed to fetch dashboard application data!"
                ).format(len(self))
                hook.post_mattermost(msg)
            raise

        exec_time = timeit.default_timer() - start
        _logger.info(
            "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
        )

    # 8. Business methods
