import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    # 1. Private attributes
    _inherit = "res.config.settings"

    # 2. Fields declaration
    message_thread_model_ids = fields.Many2many(
        related="website_id.message_thread_model_ids",
        string="Message thread models",
        help="Which models are taken into account when calculating threads",
        readonly=False,
    )
    website_enable_reply = fields.Boolean(
        string="Enable replies",
        help="If selected, users can reply to other users' messages on website",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def get_values(self):
        res = super().get_values()
        website_enable_reply = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_enable_reply", False)
        )
        res.update(
            website_enable_reply=bool(website_enable_reply),
        )
        return res

    def set_values(self):
        res = super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "website_enable_reply", bool(self.website_enable_reply)
        )
        return res

    # 7. Action methods
    def action_message_thread_init(self):
        return self.env["mail.message"].action_message_thread_init()

    # 8. Business methods
