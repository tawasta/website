from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

class AccountRequestController(http.Controller):
    @http.route('/account/request', type='json', auth="public", website=True)
    def account_request(self, email, **kw):
        if not email:
            return {'success': False, 'error': 'Email is required.'}

        # Hae kohdesähköpostiosoite järjestelmäparametreista
        target_email = request.env['ir.config_parameter'].sudo().get_param('account_request.target_email')
        system_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

        # Tarkista, että kohdesähköpostiosoite on määritelty
        if not target_email:
            return {'success': False, 'error': 'Target email for account requests is not configured.'}

        subject = "Notification: New Demo Account Request"
        body_html = """
        <p>This is a notification to inform you that a new demo account request has been received from <strong>{system_url}</strong>. The details of the request are as follows:</p>
        <ul>
            <li>Email: {email}</li>
            <li>Request Origin: {system_url}</li>
        </ul>
        <p>This notification is for your information only and no immediate action is required on your part.</p>
        """.format(email=email, system_url=system_url)
        # Lähetä sähköpostiviesti
        mail_values = {
            'subject': subject,
            'email_from': request.env.user.email_formatted,  # Lähtevän viestin lähettäjän sähköpostiosoite
            'email_to': target_email,  # Kohdesähköpostiosoite
            'body_html': body_html,
        }
        request.env['mail.mail'].sudo().create(mail_values).send()


        demo_users = request.env.ref('website_account_request.group_demo_users').users
        available_user = False
        for user in demo_users:
            if not request.session.uid or request.session.uid != user.id:
                available_user = user
                break

        if available_user:
            return {
                'success': True,
                'login': available_user.login,
                'password': available_user.login,
            }
        else:
            return {'success': False, 'error': 'No available demo accounts.'}
