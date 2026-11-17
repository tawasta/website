from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    portal_username_change_sync_partner_email = fields.Boolean(
        string="Update Contact Email on Portal Username Change",
        config_parameter="website_portal_username_change.sync_partner_email",
    )
