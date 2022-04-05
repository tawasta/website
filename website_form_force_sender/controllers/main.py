from odoo import _

from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteFormSender(WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        model_name = model.sudo().model

        if model_name == "mail.mail" and request.env.company.email:
            sender = _(f"Sent by: {values.get('email_from')}")
            # Static from company mail.
            # This could also be fetched from e.g. system parameters for more control
            values.update({"email_from": request.env.company.email})
            custom = f"{sender}\n{custom}"

        return super().insert_record(request, model, values, custom, meta)
