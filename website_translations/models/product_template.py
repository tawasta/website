from odoo import api
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, values):
        res = super().create(values)
        self._update_website_translation_values(res.id)
        return res

    @api.multi
    def write(self, values):
        res = super().write(values)
        for record in self:
            self._update_website_translation_values(record.id)

        return res

    def _update_website_translation_values(self, record_id):
        translation = self.env["ir.translation"]
        translation.translate_fields(
            "product.template", record_id, "website_description"
        )

        translations = translation.search(
            [
                ("type", "=", "model_terms"),
                ("res_id", "=", record_id),
                ("name", "like", "product.template"),
            ],
        )
        translations._compute_product_template_id()
