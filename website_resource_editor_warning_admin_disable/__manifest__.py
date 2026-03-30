##############################################################################
#
#    Author: Futural Oy
#    Copyright 2023- Futural Oy (https://futural.fi)
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
    "name": "Website Resource Editor Warning Admin Disable",
    "summary": "Disable resource editor warning for admins",
    "version": "17.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/tawasta/website",
    "author": "Futural",
    "license": "AGPL-3",
    "data": [],
    "depends": ["web"],
    "assets": {
        "web.assets_frontend_minimal": [
            "website_resource_editor_warning_admin_disable/static/src/js/resource_editor_warning.esm.js",
        ],
    },
    "application": False,
    "installable": True,
}
