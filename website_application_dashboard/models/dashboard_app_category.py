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
            endpoint_url = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("website_application_dashboard.category_endpoint", "")
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
                    "Received {} categories, create missing ones".format(len(data))
                )
                current = self.search(
                    [
                        ("category_api_id", "!=", False),
                    ]
                ).mapped("category_api_id")
                new_recs = []
                for category in data:
                    if category.get("category_id") not in current:
                        category["category_api_id"] = category.pop("category_id")
                        new_recs.append(category)

                if new_recs:
                    _logger.info("Creating {} new categories".format(len(new_recs)))
                    self.create(new_recs)

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
