from odoo.addons.website_blog.controllers.main import WebsiteBlog

import logging

_logger = logging.getLogger(__name__)


class WebsiteBlogSequence(WebsiteBlog):
    def _prepare_blog_values(
        self,
        blogs,
        blog=False,
        date_begin=False,
        date_end=False,
        tags=False,
        state=False,
        page=False,
        search=None,
        **post,
    ):
        res = super()._prepare_blog_values(
            blogs=blogs,
            blog=blog,
            date_begin=date_begin,
            date_end=date_end,
            tags=tags,
            state=state,
            page=page,
            search=search,
            **post,
        )

        # Reorder the blogs by sequence
        res["blogs"] = sorted(blogs, key=lambda blog: blog.sequence)

        return res
