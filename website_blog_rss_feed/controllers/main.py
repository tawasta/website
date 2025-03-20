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
        # Get blog posts belonging to the blogs configured in the multifeed. Extract
        # blog posts' cover images paths and mimetypes to be included in the RSS feed

        multifeed_blog_posts = (
            request.env["blog.post"]
            .with_context(lang=multifeed.lang or "en_US")
            .search(
                [
                    ("blog_id", "in", multifeed.blog_ids.ids),
                    ("is_published", "=", True),
                ],
                limit=min(int(limit), 50),
                order="post_date DESC",
            )
        )

        v = {}
        v["multifeed"] = multifeed
        v["base_url"] = multifeed.get_base_url()
        v["posts"] = multifeed_blog_posts
        v["html2plaintext"] = html2plaintext
        v["blog_images"] = {}

        for blog_post in multifeed_blog_posts:
            # this mixin function returns either "none" or "url('path-to-image')"
            blog_background = blog_post._get_background()

            if blog_background != "none":
                try:
                    # strip out the "url('" and "')" parts
                    blog_path = blog_post._get_background()[4:-1].strip("'")

                    # find the attachment record so we can read the image mimetype
                    split_path = blog_path.split("/")
                    attachment_id = split_path[3].split("-")[0]

                    image_attachment = (
                        request.env["ir.attachment"]
                        .sudo()
                        .search([["id", "=", attachment_id]])
                        .ensure_one()
                    )

                    image_info = {
                        "image_url": multifeed.get_base_url() + blog_path,
                        "image_mimetype": image_attachment.mimetype,
                    }

                    v["blog_images"][blog_post.id] = image_info

                except Exception as e:
                    _logger.error(
                        "Could not get image URL and mimetype for blog post ID %s. Attempted to parse %s. Details: "
                        % (blog_post.id, blog_post._get_background())
                    )
                    _logger.error(str(e))
                    continue

        r = request.render(
            "website_blog_rss_feed.blog_multifeed",
            v,
            headers=[("Content-Type", "application/atom+xml")],
        )
        return r
