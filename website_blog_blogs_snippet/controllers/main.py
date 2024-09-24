import logging

from odoo import fields, http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_blog.controllers.main import WebsiteBlog


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
