import logging

from odoo import api, fields, models
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

from odoo.addons.website.tools import text_from_html

_logger = logging.getLogger(__name__)


class BlogPost(models.Model):
    _inherit = "blog.post"

    paywall = fields.Boolean(
        "Paid article",
        help="Require a permission for reading the article",
    )

    paywall_description = fields.Html(related="blog_id.paywall_description")

    partner_domain_filter_ids = fields.Many2many(
        related="blog_id.partner_domain_filter_ids"
    )
    partner_free_domain_filter_ids = fields.Many2many(
        related="blog_id.partner_free_domain_filter_ids"
    )
    paywall_free_articles = fields.Integer(related="blog_id.paywall_free_articles")

    paywall_teaser = fields.Text(
        "Paywall teaser",
        compute="_compute_paywall_teaser",
    )
    paywall_teaser_length = fields.Integer("Paywall teaser length")
    user_has_access = fields.Boolean(
        string="User has access to this article", compute="_compute_user_has_access"
    )
    user_in_paywall_domain = fields.Boolean(
        string="User has access to paywall content",
        compute="_compute_user_in_paywall_domain",
    )
    user_in_paywall_free_domain = fields.Boolean(
        string="User has access to free content",
        compute="_compute_user_in_paywall_free_domain",
    )
    user_read_free_blog_post_count = fields.Integer(
        string="User blog post count",
        compute="_compute_user_read_free_blog_post_count",
    )

    @api.onchange("blog_id")
    def _compute_paywall(self):
        for record in self:
            record.paywall = record.blog_id.paywall

    @api.onchange("content", "paywall_teaser_length")
    def _compute_paywall_teaser(self):
        for record in self:
            content = text_from_html(record.content, True)
            record.paywall_teaser = content[: record.paywall_teaser_length] + "..."

    @api.onchange("blog_id")
    def _compute_paywall_teaser_length(self):
        for record in self:
            if record.paywall_teaser_length == 0:
                paywall_teaser_length = record.blog_id.paywall_teaser_length
            else:
                paywall_teaser_length = 0
            record.paywall_teaser_length = paywall_teaser_length

    def _compute_user_has_access(self):
        for record in self:
            record.user_has_access = record._user_has_access()

    def _compute_user_in_paywall_domain(self):
        partner = self.env["res.partner"].sudo()
        user_partner_id = self.env.user.partner_id.id

        for record in self:
            user_in_partner_domain = False
            for partner_domain in record.partner_domain_filter_ids:
                domain = [("id", "=", user_partner_id)] + safe_eval(
                    partner_domain.filter_domain
                )
                if partner.search(domain):
                    user_in_partner_domain = True

            record.user_in_paywall_domain = user_in_partner_domain

    def _compute_user_in_paywall_free_domain(self):
        partner = self.env["res.partner"].sudo()
        user_partner_id = self.env.user.partner_id.id

        for record in self:
            user_in_partner_domain = False
            for partner_domain in record.partner_free_domain_filter_ids:
                domain = [("id", "=", user_partner_id)] + safe_eval(
                    partner_domain.filter_domain
                )
                if partner.search(domain):
                    user_in_partner_domain = True

            record.user_in_paywall_free_domain = user_in_partner_domain

    def _compute_user_read_free_blog_post_count(self):
        for record in self:
            partner = self.env.user.partner_id
            record.user_read_free_blog_post_count = len(partner.read_free_blog_post_ids)

    def _user_has_access(self):
        # Overridable access check method
        self.ensure_one()

        if not self.paywall:
            # Allow reading for free articles
            _logger.debug("Reading allowed: No paywall")
            access = True
        elif self.env.user.has_group("website.group_website_restricted_editor"):
            # Allow reading for editors
            _logger.debug("Reading allowed: User is an editor")
            access = True
        elif self._user_is_crawler():
            # Allow reading for crawlers
            _logger.debug("Reading allowed: User is a crawler")
            access = True
        elif self.paywall and self.user_in_paywall_domain:
            # Allow reading for partners in partner domain
            _logger.debug("Reading allowed: User is an allowed user")
            access = True
        elif (
            self.paywall
            and self.user_in_paywall_free_domain
            and self._user_free_tier_available()
        ):
            # Allow reading in free tier
            _logger.debug("Reading allowed: User is in free tier")
            access = True
        else:
            # Don't allow reading
            _logger.debug("Reading disallowed")
            access = False

        return access

    def _user_free_tier_available(self):
        self.ensure_one()

        # All free tier reads are not used
        free_tier_available = (
            self.user_read_free_blog_post_count < self.paywall_free_articles
        )

        # This post is already in users free tier
        free_tier_allowed = self in self.env.user.partner_id.read_free_blog_post_ids

        res = free_tier_available or free_tier_allowed

        return res

    def _user_is_crawler(self):
        user_agent = request.httprequest.user_agent.string

        allowed_crawlers = [
            "googlebot",
            "bingbot",
            "yahoo!",
            "baiduspider",
            "yandexbot",
            "duckduckbot",
            "jeeves",
            "teoma",
            "ecosia",
        ]

        for crawler in allowed_crawlers:
            if crawler in user_agent.lower():
                return True

    def mark_post_as_read_by_user(self, user_id=False):
        self.ensure_one()
        if not user_id:
            user_id = self.env.user

        partner = user_id.partner_id

        if self not in partner.read_blog_post_ids:
            # Add blog post to all read posts
            partner.read_blog_post_ids += self

        paywall_free_domain = [("id", "=", partner.id)]
        for domain_filter in self.partner_free_domain_filter_ids:
            paywall_free_domain = paywall_free_domain + safe_eval(
                domain_filter.filter_domain
            )

        if (
            self.partner_free_domain_filter_ids
            and partner in partner.search(paywall_free_domain)
            and self not in partner.read_free_blog_post_ids
            and self.user_read_free_blog_post_count < self.paywall_free_articles
        ):
            # Add post to free tier read posts
            partner.read_free_blog_post_ids += self
            self.env.cr.commit()

        return True
