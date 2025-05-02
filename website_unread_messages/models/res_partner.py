from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_portal_needaction_count(self):
        """
        Compute the number of needaction (unread) messages in the portal.
        """
        partner = self.env.user.partner_id
        if not partner:
            _logger.error("Call to needaction_count without partner_id")
            return 0

        # Haetaan vain aktiiviset viestimallit, jos käytetään message.format sääntöä
        enabled_models = self.env["website.message.format"].search([]).mapped("res_model.model")
        
        domain = [
            ("res_partner_id", "=", partner.id),
            ("is_read", "=", False),
            ("mail_message_id.model", "in", enabled_models),
        ]
        count = self.env["mail.notification"].sudo().search_count(domain)

        return count
