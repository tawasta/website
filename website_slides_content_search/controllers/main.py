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
from collections import defaultdict

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request
from odoo.osv import expression

# 4. Imports from Odoo modules:
from odoo.addons.website_slides.controllers.main import WebsiteSlides

# 2. Known third party imports:


# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class WebsiteSlidesContentSearch(WebsiteSlides):
    @http.route("/slides/all", type="http", auth="public", website=True, sitemap=True)
    def slides_channel_all(self, slide_type=None, my=False, **post):
        """ """
        domain = request.website.website_domain()
        domain = self._build_channel_domain(
            domain, slide_type=slide_type, my=my, **post
        )

        order = self._channel_order_by_criterion.get(post.get("sorting"))

        channels = request.env["slide.channel"].search(domain, order=order)
        # channels_layouted = list(itertools.zip_longest(*[iter(channels)] * 4, fillvalue=None))

        tag_groups = request.env["slide.channel.tag.group"].search(
            ["&", ("tag_ids", "!=", False), ("website_published", "=", True)]
        )
        search_tags = self._extract_channel_tag_search(**post)

        values = self._prepare_user_values(**post)
        values.update(
            {
                "channels": channels,
                "tag_groups": tag_groups,
                "search_term": post.get("search"),
                "search_slide_type": slide_type,
                "search_my": my,
                "search_tags": search_tags,
                "search_channel_tag_id": post.get("channel_tag_id"),
                "top3_users": self._get_top3_users(),
            }
        )

        return request.render("website_slides.courses_all", values)

    def _build_channel_domain(self, base_domain, slide_type=None, my=False, **post):
        search_term = post.get("search")
        tags = self._extract_channel_tag_search(**post)

        domain = base_domain
        if search_term:
            domain = expression.AND(
                [
                    domain,
                    [
                        "|",
                        ("name", "ilike", search_term),
                        ("description", "ilike", search_term),
                    ],
                ]
            )

        if tags:
            # Group by group_id
            grouped_tags = defaultdict(list)
            for tag in tags:
                grouped_tags[tag.group_id].append(tag)

            # OR inside a group, AND between groups.
            group_domain_list = []
            for group in grouped_tags:
                group_domain_list.append(
                    [("tag_ids", "in", [tag.id for tag in grouped_tags[group]])]
                )

            domain = expression.AND([domain, *group_domain_list])
        if slide_type and "nbr_%s" % slide_type in request.env["slide.channel"]:
            domain = expression.AND([domain, [("nbr_%s" % slide_type, ">", 0)]])

        if my:
            domain = expression.AND(
                [domain, [("partner_ids", "=", request.env.user.partner_id.id)]]
            )
        return domain
