import logging

from odoo.http import request

from odoo.addons.website_blog.controllers.main import WebsiteBlog

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
        # Check if the generic blog view is being used to show the contents of a
        # single tag. If yes, pass the tag object so that its name and html description
        # will be rendered in frontend

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

        if len(res["active_tag_ids"]) == 1:
            res["show_tag_html_description"] = True
            res["active_tag_id"] = request.env["blog.tag"].search(
                [("id", "=", res["active_tag_ids"][0])]
            )
        else:
            res["show_tag_html_description"] = False

        return res
