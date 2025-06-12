##############################################################################
#
#    Author: Futural Oy
#    Copyright 2022- Futural Oy (https://futural.fi)
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
    "name": "Website Blog Tag Widget",
    "summary": "Website",
    "version": "17.0.1.0.1",
    "category": "Website",
    "website": "https://github.com/tawasta/website",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website", "website_snippet_filter_core"],
    "data": [
        "data/tagcloud_snippet_template_data.xml",
        "views/snippets/s_tagcloud.xml",
        "views/snippets/snippets.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/website_blog_tag_widget/static/src/scss/main.scss",
        ],
        "website.assets_wysiwyg": [
            "/website_blog_tag_widget/static/src/snippets/s_tagcloud/options.esm.js",
        ],
    },
}
