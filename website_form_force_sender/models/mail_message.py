from odoo import api
from odoo import models


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        print(values)

        return res
