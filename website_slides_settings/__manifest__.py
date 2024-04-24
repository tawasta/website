##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "Website Slides Settings",
    "summary": "Website Slides toggleable settings under website customize menu",
    "version": "17.0.1.0.1",
    "category": "Website/eLearning",
    "website": "https://gitlab.com/tawasta/odoo/website",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_slides", "web"],
    "data": [
        "views/website_slides_templates.xml",
        "views/res_config_settings_views.xml",
        "views/assets.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/website_slides_settings/static/src/js/slides_course_slides_list.esm.js",
        ]
    },
}
