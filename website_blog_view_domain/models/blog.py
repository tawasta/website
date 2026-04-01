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

    def _website_filter_domain(self):
        wid = self._get_current_website_id()
        if not wid:
            return []

        return [
            "|", "|",
            ("website_id", "=", False),
            ("website_id", "=", wid),
            ("website_ids", "in", [wid]),
        ]

    def _apply_website_filter(self, domain):
        domain = domain or []
        if self.env.user.has_group("website.group_website_manager"):
            return domain
        wdom = self._website_filter_domain()
        return expression.AND([domain, wdom]) if wdom else domain

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = self._apply_website_filter(args or [])
        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        domain = self._apply_website_filter(domain or [])
        return super().search(domain, offset=offset, limit=limit, order=order)

    @api.model
    def search_count(self, domain=None):
        domain = self._apply_website_filter(domain or [])
        return super().search_count(domain)

    @api.model
    def web_search_read(
        self, domain, specification, offset=0, limit=None, order=None, count_limit=None
    ):
        domain = self._apply_website_filter(domain or [])
        return super().web_search_read(
            domain,
            specification,
            offset=offset,
            limit=limit,
            order=order,
            count_limit=count_limit,
        )
