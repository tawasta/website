from odoo import http
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlogPaywall(WebsiteBlog):
    @http.route()
    def blog_post(
        self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post
    ):
        blog_post.mark_post_as_read_by_user()
        res = super().blog_post(blog, blog_post, tag_id, page, enable_editor, **post)

        return res
