from odoo import fields, models


class BlogPost(models.Model):
    _inherit = "blog.post"

    is_promoted = fields.Boolean(
        "Promoted", help="Promoted posts can be shown in a post widget."
    )
