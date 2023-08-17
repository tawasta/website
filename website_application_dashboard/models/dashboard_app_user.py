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
from odoo import _, fields, models

# import requests
# import timeit


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
        all_apps = self.env["dashboard.app"].search([])
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

    # def _get_user_data(self):
    #     """Update user data from API"""
    #     try:
    #         # endpoint_url = (
    #         #     self.env["ir.config_parameter"]
    #         #     .sudo()
    #         #     .get_param("website_application_dashboard.endpoint", "")
    #         # )
    #         # api_key = (
    #         #     self.env["ir.config_parameter"]
    #         #     .sudo()
    #         #     .get_param("website_application_dashboard.endpoint", "")
    #         # )

    #         # if endpoint_url and api_key:
    #         #     Create headers and send request
    #         #     headers = {
    #         #         "Authorization": "{}".format(api_key),
    #         #         "Accept": "application/json",
    #         #         "Content-Type": "application/json",
    #         #     }
    #         #     res = requests.get(endpoint_url, headers=headers)
    #         #     _logger.info("Response: {}".format(res.json()))
    #         pass
    #     except Exception:
    #         msg = _("Error occured when fetching user data")
    #         _logger.error(msg)
    #         raise UserError(msg) from None

    # def action_cron_update_user_data(self):
    #     """Cron to update user data from API"""
    #     _logger.info("Dashboard cron: Update user data...")
    #     try:
    #         start = timeit.default_timer()

    #         self._get_user_data()
    #         exec_time = timeit.default_timer() - start
    #         _logger.info(
    #             "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
    #         )
    #     except Exception:
    #         # Send to mattermost
    #         pass
    #         # hook = (
    #         #     self.env["mattermost.hook"]
    #         #     .sudo()
    #         #     .search(
    #         #         [
    #         #             ("res_model", "=", "dashboard.app.user"),
    #         #             ("function", "=", "get_user_app_data"),
    #         #             ("hook", "!=", False),
    #         #         ],
    #         #         limit=1,
    #         #     )
    #         # )
    #         # if hook:
    #         #     msg = (
    #         #         "### :school: Dashboard data"
    #         #         "\n Failed to fetch dashboard data!"
    #         #     ).format(len(self))
    #         #     hook.post_mattermost(msg)
    #         raise
    #     _logger.info(
    #         "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
    #     )

    # 8. Business methods
