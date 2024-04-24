from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    name_selection_based = fields.Selection(
        string="Name from Preselected Options",
        selection=[
            ("product_reservation", "Product Reservation"),
            ("resale", "Resale"),
            ("returns", "Returns"),
            ("technical_support", "Technical Support"),
            ("reclamation", "Reclamation"),
            ("feedback", "Feedback"),
            ("other", "Other Reason"),
        ],
    )

    @api.model
    def create(self, vals):
        """
        If the lead originated from website and the contact form was
        configured correctly to contain the name_selection_based field, override
        the lead name.
        """

        res = super().create(vals)

        if self._context.get("website_id") and res.name_selection_based:
            # Extract the string value of the selection that was made, e.g.
            # "other" --> "Other Reason"
            new_name = dict(
                self.env["crm.lead"].fields_get(allfields=["name_selection_based"])[
                    "name_selection_based"
                ]["selection"]
            )[res.name_selection_based]

            res.write({"name": new_name})

        return res
