import logging

from odoo import fields, models
from odoo.http import request
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    visible_website_ids = fields.Many2many(
        "website",
        string="Visible on Websites",
        index=True,
    )

    def can_access_from_current_website(self, website_id=False):
        current_id = website_id or request.env["website"].get_current_website().id
        for rec in self:
            if (
                rec.visible_website_ids
                and current_id not in rec.visible_website_ids.ids
            ):
                return False
        return True

    def search(self, args, **kwargs):
        wid = self.env.context.get("website_id")
        if wid:
            dom = expression.OR(
                [
                    [("visible_website_ids", "=", False)],
                    [("visible_website_ids", "in", [wid])],
                ]
            )
            args = expression.AND([args, dom])
        return super().search(args, **kwargs)


class BlogPost(models.Model):
    _inherit = "blog.post"

    visible_website_ids = fields.Many2many(
        "website",
        string="Visible on Websites",
        index=True,
    )

    def can_access_from_current_website(self, website_id=False):
        current_id = website_id or request.env["website"].get_current_website().id
        for rec in self:
            if (
                rec.visible_website_ids
                and current_id not in rec.visible_website_ids.ids
            ):
                return False
        return True

    def search(self, args, **kwargs):
        wid = self.env.context.get("website_id")
        if wid:
            dom = expression.OR(
                [
                    [("visible_website_ids", "=", False)],
                    [("visible_website_ids", "in", [wid])],
                ]
            )
            args = expression.AND([args, dom])
        return super().search(args, **kwargs)
