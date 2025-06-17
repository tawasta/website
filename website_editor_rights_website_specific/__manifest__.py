##############################################################################
#
#    Author: Futural Oy
#    Copyright 2024 Futural Oy (https://futural.fi)
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
    "name": "Website: Website Specific Editor Access Rights",
    "summary": "In multiwebsite environment, specify for each website who can edit it",
    "version": "17.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/tawasta/website",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website", "web_editor"],
    "data": ["views/website_views.xml"],
    "assets": {
        "website.assets_editor": [
            "website_editor_rights_website_specific/static/src/js/systray_translate_website.esm.js",
            "website_editor_rights_website_specific/static/src/js/systray_edit_website.esm.js",
        ]
    },
}
