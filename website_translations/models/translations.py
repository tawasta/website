from odoo import api, fields, models


class IrTranslation(models.Model):
    _inherit = "ir.translation"

    product_template_id = fields.Many2one(
        string="Related product",
        comodel_name="product.template",
        compute="_compute_product_template_id",
        store=True,
    )
    product_template_published = fields.Boolean(
        string="Product published",
        compute="_compute_product_template_id",
        store=True,
    )

    product_template_updated = fields.Datetime(string="Product template updated")

    website_page_id = fields.Many2one(
        string="Website page",
        comodel_name="website.page",
        compute="_compute_website_page_id",
        store=True,
    )
    website_page_updated = fields.Datetime(string="Website page updated")

    @api.depends("res_id")
    def _compute_product_template_id(self):
        product_template = self.env["product.template"]
        for record in self:
            try:
                model, field = record.name.split(",")

                if model == "product.template":
                    product = product_template.with_context(active_test=False).browse(
                        record.res_id
                    )
                    if product:
                        record.product_template_id = product.id
                        record.product_template_updated = fields.Datetime.now()
                        record.product_template_published = (
                            product.website_published and product.active
                        )
            except ValueError:
                # Skip translations with incomplete data
                continue

    @api.depends("res_id")
    def _compute_website_page_id(self):
        view_model = self.env["ir.ui.view"]

        # TODO: support multi-website
        homepage = self.env["website.page"].search([("url", "=", "/")], limit=1)

        for record in self:
            website_page_id = False
            if record.type == "model_terms" and record.name == "ir.ui.view,arch_db":
                view = view_model.search(
                    [("id", "=", record.res_id), ("type", "=", "qweb")], limit=1
                )

                if view:
                    first_page = self.env["website.page"].search(
                        [("view_id", "=", view.id)], limit=1
                    )
                    if first_page:
                        website_page_id = first_page.id
                    elif "website" in view.key:
                        website_page_id = homepage.id

            record.website_page_updated = fields.Datetime.now()
            record.website_page_id = website_page_id
