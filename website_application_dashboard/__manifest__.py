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

{
    "name": "Website Application Dashboard",
    "summary": "Application dashboard for redirecting users to applications",
    "version": "17.0.1.1.0",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/website",
    "author": "Tawasta",
    "license": "AGPL-3",
    "data": [
        "data/ir_cron.xml",
        "data/dashboard_app_category_data.xml",
        "data/website_data.xml",
        "data/ir_config_parameter_data.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "security/application_security.xml",
        "views/dashboard_app_views.xml",
        "views/dashboard_app_user_views.xml",
        "views/dashboard_app_category_views.xml",
        "views/website_views.xml",
        "views/website_dashboard.xml",
    ],
    "depends": [
        "website",
        "mattermost_hook",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "website_application_dashboard/static/src/scss/primary_variable.scss",
        ],
        "web.assets_frontend": [
            "website_application_dashboard/static/src/scss/dashboard.scss",
            "website_application_dashboard/static/src/js/dashboard.esm.js",
        ],
    },
    "application": False,
    "installable": True,
}
