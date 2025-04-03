##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "Website Banner",
    "summary": "Website",
    "version": "17.0.1.0.1",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/website",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website"],
    "data": [
        "security/ir.model.access.csv",
        "data/advertisement_snippet_template_data.xml",
        "views/snippets/s_advertisement.xml",
        "views/snippets/snippets.xml",
        "views/advertisement_view.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/website_banner/static/src/scss/main.scss",
            "/website_banner/static/src/js/tracker.esm.js",
        ],
        "website.assets_wysiwyg": [
            "/website_banner/static/src/snippets/s_advertisement/options.esm.js",
        ],
    },
}
