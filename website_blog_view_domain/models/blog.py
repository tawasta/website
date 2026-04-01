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
            "[blog.blog] Current website resolved: "
            "website=%s wid=%s user=%s(%s)",
            website.display_name if website else None,
            wid,
            self.env.user.login,
            self.env.user.id,
        )
        return wid

    def _is_website_manager(self):
        is_manager = self.env.user.has_group(
            "website_manager_group.group_website_manager"
        )
        _logger.warning(
            "[blog.blog] _is_website_manager: user=%s(%s) manager=%s",
            self.env.user.login,
            self.env.user.id,
            is_manager,
        )
        return is_manager

    def _website_filter_domain(self):
        wid = self._get_current_website_id()
        if not wid:
            _logger.warning(
                "[blog.blog] No current website found, returning empty domain"
            )
            return []

        is_manager = self._is_website_manager()
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
                    "[blog.blog] Field visible_website_ids not found on "
                    "blog.blog, fallback domain used"
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
            "[blog.blog] Apply website filter: original_domain=%s "
            "website_domain=%s final_domain=%s",
            domain,
            wdom,
            final_domain,
        )
        return final_domain

    def _search_env_for_test(self):
        is_manager = self._is_website_manager()
        if is_manager:
            _logger.warning(
                "[blog.blog] Using sudo() for manager search in test"
            )
            return self.sudo()
        return self

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        _logger.warning(
            "[blog.blog] RAW name_search incoming: name=%s args=%s "
            "operator=%s limit=%s",
            name,
            args,
            operator,
            limit,
        )

        args = self._apply_website_filter(args or [])

        _logger.warning(
            "[blog.blog] FILTERED name_search: name=%s args=%s "
            "operator=%s limit=%s",
            name,
            args,
            operator,
            limit,
        )

        model = self._search_env_for_test()
        res = super(BlogBlog, model).name_search(
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
        _logger.warning(
            "[blog.blog] RAW search incoming: domain=%s offset=%s "
            "limit=%s order=%s",
            domain,
            offset,
            limit,
            order,
        )

        domain = self._apply_website_filter(domain or [])

        _logger.warning(
            "[blog.blog] FILTERED search: domain=%s offset=%s "
            "limit=%s order=%s",
            domain,
            offset,
            limit,
            order,
        )

        model = self._search_env_for_test()
        res = super(BlogBlog, model).search(
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

        for blog in res:
            _logger.warning(
                "[blog.blog] result record: id=%s name=%s "
                "website_id=%s visible_website_ids=%s",
                blog.id,
                blog.display_name,
                blog.website_id.id if blog.website_id else False,
                (
                    blog.visible_website_ids.ids
                    if "visible_website_ids" in blog._fields
                    else []
                ),
            )

        return res

    @api.model
    def search_count(self, domain=None):
        _logger.warning(
            "[blog.blog] RAW search_count incoming: domain=%s",
            domain,
        )

        domain = self._apply_website_filter(domain or [])

        _logger.warning(
            "[blog.blog] FILTERED search_count: domain=%s",
            domain,
        )

        model = self._search_env_for_test()
        res = super(BlogBlog, model).search_count(domain)

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
        _logger.warning(
            "[blog.blog] RAW web_search_read incoming: domain=%s "
            "spec_keys=%s offset=%s limit=%s order=%s count_limit=%s",
            domain,
            list(specification.keys()) if specification else [],
            offset,
            limit,
            order,
            count_limit,
        )

        domain = self._apply_website_filter(domain or [])

        _logger.warning(
            "[blog.blog] FILTERED web_search_read: domain=%s",
            domain,
        )

        model = self._search_env_for_test()
        res = super(BlogBlog, model).web_search_read(
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