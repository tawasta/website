from odoo import fields, models


class BlogPost(models.Model):
    _inherit = "blog.post"

    paid_article = fields.Boolean(
        "Paid article",
        help="Require a permission for reading the article",
        default=False,
    )

    user_has_access = fields.Boolean(
        string="User has access to this article", compute="_compute_user_has_access"
    )

    def _compute_user_has_access(self):
        for record in self:
            record.user_has_access = record._user_has_access()

    def _user_has_access(self):
        # Overridable access check method
        self.ensure_one()

        access = False

        if not self.paid_article or not self.env.user._is_public():
            # Free article or logged-in user
            access = True

        return access
