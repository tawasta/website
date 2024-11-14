from odoo import models


class IrQWeb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _prepare_frontend_environment(self, values):
        # Show the Translate button in frontend systray for Restricted Editor group
        # users

        irQweb = super()._prepare_frontend_environment(values)

        user_only_restricted_editor = irQweb.env.user.has_group(
            "website.group_website_restricted_editor"
        ) and not irQweb.env.user.has_group("website.group_website_designer")
        viewing_different_lang = (
            irQweb.env.context.get("lang")
            != irQweb.env["ir.http"]._get_default_lang().code
        )

        if user_only_restricted_editor and viewing_different_lang:
            values["translatable"] = True

        return irQweb
