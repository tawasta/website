from odoo import fields, models


class ResReferencesCategory(models.Model):
    _name = "res.references.category"
    _description = "Reference Category"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class ResReferences(models.Model):
    _name = "res.references"
    _description = "References"
    _order = "featured desc, sequence asc, id asc"

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    image = fields.Image()
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    link = fields.Char(string="Website Link")
    button_link = fields.Char()

    category_ids = fields.Many2many(
        "res.references.category",
        "res_references_category_rel",
        "reference_id",
        "category_id",
        string="Categories",
    )

    featured = fields.Boolean(default=False)
