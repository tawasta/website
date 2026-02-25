from odoo import models, api


class BlogPost(models.Model):
    _inherit = "blog.post"

    @api.onchange("website_id")
    def _onchange_blog_id_domain(self):
        if self.env.user.has_group("website_manager_group.group_website_manager"):
            return {}

        website_id = self.env.context.get("website_id")
        return {
            "domain": {
                "blog_id": [
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", website_id),
                ]
            }
        }