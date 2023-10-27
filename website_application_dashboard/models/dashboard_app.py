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

import base64

# 1. Standard library imports:
import logging
import timeit

# 3. Odoo imports (openerp):
from odoo import _, fields, models, tools
from odoo.exceptions import UserError
from odoo.modules.module import get_resource_path

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

    # 2. Fields declaration
    def _default_logo(self):
        image_path = get_resource_path(
            "website_application_dashboard", "static/description", "icon.png"
        )
        with tools.file_open(image_path, "rb") as f:
            return base64.b64encode(f.read())

    name = fields.Char(
        help="Name of the application",
        required=True,
    )
    info = fields.Html(
        help="Info for the application",
        translate=True,
        sanitize=False,
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
            result = [
                {
                    "name": "Iltasanomat",
                    "info": "Tässä infoa iltasanomiin liittyen",
                    "description": "Sovelluksen kuvausta...",
                    "url": "https://is.fi",
                    "application_api_id": 53,
                },
                {
                    "name": "Google",
                    "info": "Tässä infoa Googleen liittyen",
                    "description": "Sovelluksen kuvausta...",
                    "url": "https://google.com",
                    "application_api_id": 87,
                },
            ]
            self.create(result)
            # endpoint_url = (
            #     self.env["ir.config_parameter"]
            #     .sudo()
            #     .get_param("website_application_dashboard.endpoint", "")
            # )
            # api_key = (
            #     self.env["ir.config_parameter"]
            #     .sudo()
            #     .get_param("website_application_dashboard.endpoint", "")
            # )

            # if endpoint_url and api_key:
            #     Create headers and send request
            #     headers = {
            #         "Authorization": "{}".format(api_key),
            #         "Accept": "application/json",
            #         "Content-Type": "application/json",
            #     }
            #     res = requests.get(endpoint_url, headers=headers)
            #     _logger.info("Response: {}".format(res.json()))
        except Exception:
            msg = _("Error occured when fetching user data")
            _logger.error(msg)
            raise UserError(msg) from None

    def action_cron_update_applications(self):
        """Cron to update user data from API"""
        _logger.info("Dashboard cron: Update applications...")
        try:
            start = timeit.default_timer()

            self._get_applications()
            exec_time = timeit.default_timer() - start
            _logger.info(
                "Dashboard cron: total execution in {:.2f} seconds!".format(exec_time)
            )
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

    # 8. Business methods
