from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class BlogPost(models.Model):
    _inherit = "blog.post"

    paywall = fields.Boolean(
        "Paid article",
        help="Require a permission for reading the article",
    )

    paywall_description = fields.Html(related="blog_id.paywall_description")

    paywall_domain = fields.Char(related="blog_id.paywall_domain")

    user_has_access = fields.Boolean(
        string="User has access to this article", compute="_compute_user_has_access"
    )

    @api.onchange("blog_id")
    def _compute_paywall(self):
        for record in self:
            record.paywall = record.blog_id.paywall

    def _compute_user_has_access(self):
        for record in self:
            record.user_has_access = record._user_has_access()

    def _user_has_access(self):
        # Overridable access check method
        self.ensure_one()
        partner = self.env["res.partner"].sudo()
        partner_id = self.env.user.partner_id.id
        domain = [("id", "=", partner_id)] + safe_eval(self.paywall_domain)

        if not self.paywall:
            # Allow reading for free articles
            access = True
        elif self.paywall and partner.search(domain):
            # Allow reading for partners in partner domain
            access = True
        else:
            # Don't allow reading
            access = False

        return access

    def read(self, fields=None, load="_classic_read"):
        print(self)
        print(fields)
        print("Reading this post")
        return super().read(fields=fields, load=load)
