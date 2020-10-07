from odoo import models
from odoo import fields


class IrTranslation(models.Model):
    _inherit = "ir.translation"

    product_template_id = fields.Many2one(
        string="Related product",
        comodel_name="product.template",
        compute="_compute_product_template_id",
    )

    def _compute_product_template_id(self):
        product_template = self.env["product.template"]
        for record in self:
            try:
                model, field = record.name.split(",")

                if model == "product.template":
                    product = product_template.browse(record.res_id)
                    if product:
                        record.product_template_id = product.id
            except ValueError:
                # Skip translations with incomplete data
                continue
