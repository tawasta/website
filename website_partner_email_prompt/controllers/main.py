from odoo import http, _
from odoo.http import request


class PartnerEmailPrompt(http.Controller):

    @http.route('/my/email_check', type='json', auth="user", website=True)
    def email_check(self):
        """Check if the logged-in user's partner has an email."""
        partner = request.env.user.partner_id
        if not partner.email:
            return request.env['ir.ui.view']._render_template(
                "website_partner_email_prompt.modal_email_form", {'partner': partner}
            )
        return False

    @http.route('/my/email_update', type='json', auth="user", methods=['POST'], website=True)
    def email_update(self, email=None):
        """Update the partner's email."""
        partner = request.env.user.partner_id
        if email:
            partner.sudo().write({'email': email})
            return {
                'success': True,
                'message': _('Your email has been successfully updated!')
            }
        return {
            'success': False,
            'error': _('Invalid email address. Please try again.')
        }
