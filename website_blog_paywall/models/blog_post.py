from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
from odoo.addons.website.tools import text_from_html


class BlogPost(models.Model):
    _inherit = "blog.post"

    paywall = fields.Boolean(
        "Paid article",
        help="Require a permission for reading the article",
    )

    paywall_description = fields.Html(related="blog_id.paywall_description")

    paywall_domain = fields.Char(related="blog_id.paywall_domain")
    paywall_free_domain = fields.Char(related="blog_id.paywall_free_domain")
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
        partner_id = self.env.user.partner_id.id

        for record in self:
            paywall_domain = False
            if record.paywall_domain:
                paywall_domain = [("id", "=", partner_id)] + safe_eval(
                    record.paywall_domain
                )

            if paywall_domain and partner.search(paywall_domain):
                record.user_in_paywall_domain = True
            else:
                record.user_in_paywall_domain = False

    def _compute_user_in_paywall_free_domain(self):
        partner = self.env["res.partner"].sudo()
        partner_id = self.env.user.partner_id.id

        for record in self:
            paywall_free_domain = False
            if self.paywall_free_domain:
                paywall_free_domain = [("id", "=", partner_id)] + safe_eval(
                    self.paywall_free_domain
                )

            if paywall_free_domain and partner.search(paywall_free_domain):
                record.user_in_paywall_free_domain = True
            else:
                record.user_in_paywall_free_domain = False

    def _compute_user_read_free_blog_post_count(self):
        for record in self:
            partner = self.env.user.partner_id
            record.user_read_free_blog_post_count = len(partner.read_free_blog_post_ids)

    def _user_has_access(self):
        # Overridable access check method
        self.ensure_one()

        if not self.paywall:
            # Allow reading for free articles
            access = True
        elif self.env.user.has_group("website.group_website_restricted_editor"):
            # Allow reading for editors
            access = True
        elif self.paywall and self.user_in_paywall_domain:
            # Allow reading for partners in partner domain
            access = True
        elif (
            self.paywall
            and self.user_in_paywall_free_domain
            and self._user_free_tier_available()
        ):
            # Allow reading in free tier
            access = True
        else:
            # Don't allow reading
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

    def mark_post_as_read_by_user(self, user_id=False):
        self.ensure_one()
        if not user_id:
            user_id = self.env.user

        partner = user_id.partner_id

        if self not in partner.read_blog_post_ids:
            # Add blog post to all read posts
            partner.read_blog_post_ids += self

        paywall_free_domain = False
        if self.paywall_free_domain:
            paywall_free_domain = [("id", "=", partner.id)] + safe_eval(
                self.paywall_free_domain
            )

        if (
            paywall_free_domain
            and partner in partner.search(paywall_free_domain)
            and self not in partner.read_free_blog_post_ids
            and self.user_read_free_blog_post_count < self.paywall_free_articles
        ):
            # Add post to free tier read posts
            partner.read_free_blog_post_ids += self
            self.env.cr.commit()

        return True
