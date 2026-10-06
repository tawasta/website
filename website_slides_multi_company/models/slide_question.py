from odoo import fields, models


class SlideQuestion(models.Model):
    _inherit = "slide.question"

    company_id = fields.Many2one(
        "res.company",
        related="slide_id.company_id",
        store=True,
        index=True,
    )


class SlideAnswer(models.Model):
    _inherit = "slide.answer"

    company_id = fields.Many2one(
        "res.company",
        related="question_id.company_id",
        store=True,
        index=True,
    )
