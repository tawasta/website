##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 2. Known third party imports:

import logging

# 3. Odoo imports (openerp):
from odoo import fields, http
from odoo.http import request
from odoo.osv import expression

# 4. Imports from Odoo modules:
from odoo.addons.website_blog.controllers.main import WebsiteBlog

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class WebsiteBlogSnippet(WebsiteBlog):
    @http.route(["/blog/render_latest_posts"], type="json", auth="public", website=True)
    def render_latest_posts(
        self, template, domain, limit=None, columns=None, order="published_date desc"
    ):
        """Override the entire function as we are adding a 6th argument"""
        dom = expression.AND(
            [
                [
                    ("website_published", "=", True),
                    ("post_date", "<=", fields.Datetime.now()),
                ],
                request.website.website_domain(),
            ]
        )
        if domain:
            dom = expression.AND([dom, domain])
        logging.info(limit)
        posts = request.env["blog.post"].search(dom, limit=limit, order=order)
        logging.info(posts)
        return request.website.viewref(template)._render(
            {"posts": posts, "columns": columns}
        )
