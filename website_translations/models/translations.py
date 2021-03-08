from odoo import api
from odoo import models
from odoo import fields


class IrTranslation(models.Model):
    _inherit = "ir.translation"

    product_template_id = fields.Many2one(
        string="Related product",
        comodel_name="product.template",
        compute="_compute_product_template_id",
    )

    website_page_id = fields.Many2one(
        string="Website page",
        comodel_name="website.page",
        compute="_compute_website_page_id",
        store=True,
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

    @api.depends("res_id")
    def _compute_website_page_id(self):
        view_model = self.env["ir.ui.view"]
        for record in self:
            if record.type == "model_terms" and not record.module:
                view = view_model.search(
                    [
                        ("id", "=", record.res_id),
                        ("type", "=", "qweb"),
                        ("first_page_id", "!=", False),
                    ]
                )

                if view and len(view) == 1:
                    record.first_page_id = self.env["website.page"].search(
                        [("view_id", "=", view.id)], limit=1
                    )
            else:
                record.website_page_id = False
