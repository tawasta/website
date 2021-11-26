##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
import urllib.request, io

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request
from odoo.tools import html2plaintext

# 4. Imports from Odoo modules:
from odoo.addons.website_blog.controllers.main import WebsiteBlog

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


def split_css_url(attribute):
    return attribute.split("'")[1]


def get_filesize_from_url(url):
    path = urllib.request.urlopen(url)
    meta = path.info()
    return meta.get(name="Content-Length")


def get_filetype_from_url(url):
    path = urllib.request.urlopen(url)
    meta = path.info()
    return meta.get(name="Content-Type")


class WebsiteBlogRssFeed(WebsiteBlog):
    @http.route(
        ["""/blog/<model("blog.blog"):blog>/feed"""],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def blog_feed(self, blog, limit="15", **kwargs):
        v = {}
        v["blog"] = blog
        v["base_url"] = blog.get_base_url()
        v["posts"] = request.env["blog.post"].search(
            [("blog_id", "=", blog.id)],
            limit=min(int(limit), 50),
            order="post_date DESC",
        )
        v["html2plaintext"] = html2plaintext
        v["split_css_url"] = split_css_url
        v["get_filesize_from_url"] = get_filesize_from_url
        v["get_filetype_from_url"] = get_filetype_from_url
        r = request.render(
            "website_blog.blog_feed",
            v,
            headers=[("Content-Type", "application/atom+xml")],
        )
        return r
