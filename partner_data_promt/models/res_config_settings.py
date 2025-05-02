from odoo import models, fields, api

class Website(models.Model):
    _inherit = "website"

    data_prompt_interval_days = fields.Integer(
        string="Data Prompt Interval (days)",
        default=30,
        help="Number of days between data prompts on this website."
    )

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    data_prompt_interval_days = fields.Integer(
        string="Data Prompt Interval (Days)",
        related="website_id.data_prompt_interval_days",
        default=90,
        help="Show the profile update modal again if the last check is older than this many days.",
    )
