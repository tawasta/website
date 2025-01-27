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
    "name": "Website Blog Blogs Snippet (DEPRECATED)",
    "summary": "Improved Blogs Snippets (deprecated)",
    "version": "17.0.2.0.0",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/website",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": ["web", "website_blog"],
    "data": ["views/website_blog_views.xml", "views/snippets/s_latest_posts.xml"],
    "assets": {
        "web.assets_frontend": [
            "/website_blog_blogs_snippet/static/src/js/s_latest_posts.esm.js",
            "/website_blog_blogs_snippet/static/src/scss/s_latest_posts.scss",
        ]
    },
}
