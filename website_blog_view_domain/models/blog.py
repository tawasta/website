import logging

from odoo import api, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    def _get_current_website_id(self):
        website = self.env["website"].get_current_website()
        wid = website.id if website else False
        _logger.warning(
            "[blog.blog] Current website resolved: website=%s wid=%s " "user=%s(%s)",
            website.display_name if website else None,
            wid,
            self.env.user.login,
            self.env.user.id,
        )
        return wid

    def _website_filter_domain(self):
        wid = self._get_current_website_id()
        if not wid:
            _logger.warning(
                "[blog.blog] No current website found, returning empty domain"
            )
            return []

        is_manager = self.env.user.has_group("website_manager_group.group_website_manager")
        has_visible_websites = "visible_website_ids" in self._fields

        _logger.warning(
            "[blog.blog] Building website filter: user=%s(%s) "
            "manager=%s visible_website_ids_exists=%s website_id=%s",
            self.env.user.login,
            self.env.user.id,
            is_manager,
            has_visible_websites,
            wid,
        )

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
                _logger.warning(
                    "[blog.blog] Field visible_website_ids not found "
                    "on blog.blog, fallback domain used"
                )
                domain = [
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", wid),
                ]

            _logger.warning(
                "[blog.blog] Manager domain: %s",
                domain,
            )
            return domain

        domain = [("website_id", "=", wid)]
        _logger.warning(
            "[blog.blog] Normal user domain: %s",
            domain,
        )
        return domain

    def _apply_website_filter(self, domain):
        domain = domain or []
        wdom = self._website_filter_domain()
        final_domain = expression.AND([domain, wdom]) if wdom else domain

        _logger.warning(
            "[blog.blog] Apply website filter: "
            "original_domain=%s website_domain=%s final_domain=%s",
            domain,
            wdom,
            final_domain,
        )
        return final_domain

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = self._apply_website_filter(args or [])
        _logger.warning(
            "[blog.blog] name_search called: name=%s operator=%s " "limit=%s args=%s",
            name,
            operator,
            limit,
            args,
        )
        res = super().name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
        )
        _logger.warning(
            "[blog.blog] name_search result count=%s result=%s",
            len(res),
            res,
        )
        return res

    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        domain = self._apply_website_filter(domain or [])
        _logger.warning(
            "[blog.blog] search called: domain=%s offset=%s " "limit=%s order=%s",
            domain,
            offset,
            limit,
            order,
        )
        res = super().search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )
        _logger.warning(
            "[blog.blog] search result ids=%s count=%s",
            res.ids,
            len(res),
        )
        return res

    @api.model
    def search_count(self, domain=None):
        domain = self._apply_website_filter(domain or [])
        _logger.warning(
            "[blog.blog] search_count called: domain=%s",
            domain,
        )
        res = super().search_count(domain)
        _logger.warning(
            "[blog.blog] search_count result=%s",
            res,
        )
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
        _logger.warning(
            "[blog.blog] web_search_read called: domain=%s "
            "spec_keys=%s offset=%s limit=%s order=%s "
            "count_limit=%s",
            domain,
            list(specification.keys()) if specification else [],
            offset,
            limit,
            order,
            count_limit,
        )
        res = super().web_search_read(
            domain,
            specification,
            offset=offset,
            limit=limit,
            order=order,
            count_limit=count_limit,
        )
        _logger.warning(
            "[blog.blog] web_search_read result=%s",
            res,
        )
        return res
