import logging

from odoo import api, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    def _get_current_website_id(self):
        website = self.env["website"].get_current_website()
        wid = website.id if website else False
        return wid

    def _is_website_manager(self):
        is_manager = self.env.user.has_group(
            "website_manager_group.group_website_manager"
        )
        return is_manager

    def _website_filter_domain(self):
        wid = self._get_current_website_id()
        if not wid:
            return []

        is_manager = self._is_website_manager()
        has_visible_websites = "visible_website_ids" in self._fields

        if is_manager:
            if has_visible_websites:
                domain = [
                    "|",
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", wid),
                    ("visible_website_ids", "in", [wid]),
                ]
            else:
                domain = [
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", wid),
                ]

            return domain

        domain = [("website_id", "=", wid)]
        return domain

    def _apply_website_filter(self, domain):
        domain = domain or []
        wdom = self._website_filter_domain()
        final_domain = expression.AND([domain, wdom]) if wdom else domain

        return final_domain

    def _search_env_for_test(self):
        is_manager = self._is_website_manager()
        if is_manager:
            return self.sudo()
        return self

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = self._apply_website_filter(args or [])

        model = self._search_env_for_test()
        res = super(BlogBlog, model).name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
        )

        return res

    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        domain = self._apply_website_filter(domain or [])

        model = self._search_env_for_test()
        res = super(BlogBlog, model).search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )

        return res

    @api.model
    def search_count(self, domain=None):
        domain = self._apply_website_filter(domain or [])

        model = self._search_env_for_test()
        res = super(BlogBlog, model).search_count(domain)

        return res

    @api.model
    def web_search_read(
        self,
        domain,
        specification,
        offset=0,
        limit=None,
        order=None,
        count_limit=None,
    ):
        domain = self._apply_website_filter(domain or [])

        model = self._search_env_for_test()
        res = super(BlogBlog, model).web_search_read(
            domain,
            specification,
            offset=offset,
            limit=limit,
            order=order,
            count_limit=count_limit,
        )

        return res
