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

# 3. Odoo imports (openerp):
from odoo import _, fields, models

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


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
        )
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

    # 8. Business methods
