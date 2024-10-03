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

import logging

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request
from odoo.tools import html2plaintext

# 4. Imports from Odoo modules:
from odoo.addons.website_blog.controllers.main import WebsiteBlog

# 1. Standard library imports:


# 2. Known third party imports:


# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class WebsiteBlogRssMultifeed(WebsiteBlog):
    @http.route(
        ["""/feed/<model("blog.multifeed"):multifeed>"""],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def blog_multi_feed(self, multifeed, limit="15", **kwargs):
        v = {}
        v["multifeed"] = multifeed
        v["base_url"] = multifeed.get_base_url()
        v["posts"] = request.env["blog.post"].search(
            [("blog_id", "in", multifeed.blog_ids.ids)],
            limit=min(int(limit), 50),
            order="post_date DESC",
        )
        v["html2plaintext"] = html2plaintext
        r = request.render(
            "website_blog_rss_feed.blog_multifeed",
            v,
            headers=[("Content-Type", "application/atom+xml")],
        )
        return r
