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

import logging
import sys
import timeit
import traceback

# 1. Standard library imports:
import requests

# 3. Odoo imports (openerp):
from odoo import _, fields, models
from odoo.exceptions import UserError

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class DashboardAppCategory(models.Model):
    # 1. Private attributes
    _name = "dashboard.app.category"
    _description = "Dashboard Application Category"
    _order = "sequence, id"
    _sql_constraints = [
        (
            "dashboard_category_uniq",
            "unique (name)",
            _("Application category already exists!"),
        ),
        (
            "dashboard_category_api_id_uniq",
            "unique (category_api_id)",
            _("Application category API id already exists!"),
        ),
    ]

    # 2. Fields declaration
    sequence = fields.Integer(
        help="Used to order categories for applications",
        default=1,
    )
    name = fields.Char(
        help="Category name for different applications",
    )
    application_ids = fields.One2many(
        comodel_name="dashboard.app",
        inverse_name="category_id",
        string="Applications",
        help="Applications belonging to this category",
    )
    category_api_id = fields.Integer(
        string="API ID",
        help="Category ID in API",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_category_data(self):
        """Update category data from API"""
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
                    "website_application_dashboard.category_endpoint{}".format(
                        api_suffix
                    ),
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
                    "Received {} categories, create missing ones".format(len(data))
                )
                current = self.search(
                    [
                        ("category_api_id", "!=", False),
                    ]
                )
                current_api_ids = current.mapped("category_api_id")
                new_recs = []
                handled = self.env["dashboard.app.category"]
                for rec_data in data:
                    category_id = rec_data.pop("category_id")
                    if not category_id:
                        _logger.error("No category ID provided: {}".format(rec_data))
                        continue

                    if category_id not in current_api_ids:
                        rec_data["category_api_id"] = category_id
                        duplicate = self.search([("name", "=", rec_data.get("name"))])
                        if len(duplicate) > 0:
                            _logger.error(
                                "Duplicate for category was found"
                                " with name {}, skipping...".format(
                                    rec_data.get("name")
                                )
                            )
                            continue

                        new_recs.append(rec_data)
                    else:
                        # Update category info
                        rec = self.search(
                            [("category_api_id", "=", category_id)], limit=1
                        )
                        rec.write(rec_data)
                        handled |= rec

                if new_recs:
                    _logger.info("Creating {} new categories".format(len(new_recs)))
                    handled |= self.create(new_recs)

                removed_recs = current - handled
                if removed_recs:
                    _logger.info("Removing categories {}...".format(removed_recs))
                    removed_recs.unlink()

        except Exception:
            msg = _("Error occured when fetching category data")
            _logger.error(msg)
            info = sys.exc_info()
            formatted_info = "".join(traceback.format_exception(*info))
            _logger.error(formatted_info)
            raise UserError(msg) from None

    def action_cron_update_category_data(self):
        """Cron to update category data from API"""
        _logger.info("Dashboard cron: Update category data...")
        start = timeit.default_timer()
        try:
            self._get_category_data()
        except Exception:
            # Send to mattermost
            _logger.error("Dashboard cron: sending error message to mattermost...")
            hook = (
                self.env["mattermost.hook"]
                .sudo()
                .search(
                    [
                        ("res_model", "=", "dashboard.app.category"),
                        ("function", "=", "_get_category_data"),
                        ("hook", "!=", False),
                    ],
                    limit=1,
                )
            )
            if hook:
                msg = _(
                    "### :no_entry: Dashboard category data"
                    "\n Failed to fetch dashboard category data!"
                ).format(len(self))
                hook.post_mattermost(msg)
            raise

        exec_time = timeit.default_timer() - start
        _logger.info(
            "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
        )

    # 8. Business methods
