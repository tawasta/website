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


class DashboardAppUser(models.Model):

    # 1. Private attributes
    _name = "dashboard.app.user"
    _description = "Dashboard Application"
    _order = "sequence, id"
    _rec_name = "application_id"
    _sql_constraints = [
        (
            "user_app_uniq",
            "unique (application_id,user_id)",
            _("User data for this application already exists!"),
        )
    ]

    # 2. Fields declaration
    sequence = fields.Integer(
        help="Used to order dashboard application for user",
        default=1,
    )
    application_id = fields.Many2one(
        comodel_name="dashboard.app",
        string="Application",
        help="What application this user info is related to",
        required=True,
    )
    category_id = fields.Many2one(
        comodel_name="dashboard.app.category",
        string="Category",
        help="To what category this application belongs to",
        related="application_id.category_id",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        help="What user this application info is related to",
        required=True,
    )
    visible = fields.Boolean(
        help="Is this application visible to the user",
        default=True,
    )
    notification_count = fields.Integer(
        string="Notifications",
        help="How many notifications user has",
    )
    url = fields.Char(
        help="User specific URL",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def get_user_apps(self, user_id):
        """
        Get user apps in specific order
        :param user_id: ID
        :return: recordset
        """
        all_apps = self.env["dashboard.app"].search(
            [
                "|",
                ("user_id", "=", False),
                ("user_id", "=", self.env.uid),
            ]
        )
        _logger.info("Found {} applications".format(len(all_apps)))
        user_datas = self.search([("user_id", "=", user_id)])
        user_apps = user_datas.mapped("application_id")

        for app in all_apps:
            if app not in user_apps:
                user_datas |= self.create(
                    {
                        "application_id": app.id,
                        "user_id": user_id,
                    }
                )
        return user_datas

    def _get_user_data(self):
        """Update user data from API"""
        try:
            endpoint_url = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("website_application_dashboard.user_endpoint", "")
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
                    "Received {} user datas, update user datas".format(len(data))
                )

                for el in data:
                    email = el.get("user_uid")
                    user = self.env["res.users"].search(
                        [
                            ("email", "=", email),
                        ],
                        limit=1,
                    )
                    application = self.env["dashboard.app"].search(
                        [
                            ("application_api_id", "=", el.get("application_id")),
                        ],
                        limit=1,
                    )
                    if not user:
                        msg = _("User not found with email {}").format(email)
                        _logger.error(msg)
                        continue

                    if not application:
                        msg = _("Application not found with ID {}").format(
                            el.get("application_id")
                        )
                        _logger.error(msg)
                        continue

                    vals = {}
                    if el.get("notification_count"):
                        vals["notification_count"] = el.get("notification_count")
                    if el.get("url"):
                        vals["url"] = el.get("url")

                    user_data = self.env["dashboard.app.user"].search(
                        [
                            ("user_id", "=", user.id),
                            ("application_id", "=", application.id),
                        ]
                    )
                    if user_data:
                        user_data.update(vals)
                    else:
                        vals.update(
                            {
                                "user_id": user.id,
                                "application_id": application.id,
                            }
                        )
                        self.create(vals)
        except Exception:
            msg = _("Error occured when fetching user data")
            _logger.error(msg)
            info = sys.exc_info()
            formatted_info = "".join(traceback.format_exception(*info))
            _logger.error(formatted_info)
            raise UserError(msg) from None

    def action_cron_update_user_data(self):
        """Cron to update user data from API"""
        _logger.info("Dashboard cron: Update user data...")
        start = timeit.default_timer()
        try:
            self._get_user_data()
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
            #         "### :school: Dashboard data user"
            #         "\n Failed to fetch dashboard data!"
            #     ).format(len(self))
            #     hook.post_mattermost(msg)
            raise

        exec_time = timeit.default_timer() - start
        _logger.info(
            "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
        )

    # 8. Business methods
