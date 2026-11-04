from odoo import fields, models


class ForumForum(models.Model):
    _inherit = "forum.forum"

    show_question_example = fields.Boolean(
        string="Show Question Title Example",
        default=True,
        help="Show an example of a good and a bad question title "
        "on the new question form.",
    )
