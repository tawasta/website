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

# 3. Odoo imports (openerp):
from odoo import fields, models, tools
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
    )
    logo = fields.Binary(
        default=_default_logo,
        help="Display this logo for the application.",
    )
    info = fields.Text(
        help="Info for the application",
    )
    description = fields.Text(
        help="Description for the application",
    )
    url = fields.Char(
        help="URL for the application",
    )
    app_user_ids = fields.One2many(
        comodel_name="dashboard.app.user",
        inverse_name="application_id",
        string="Application user datas",
        help="User datas related to this application",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
