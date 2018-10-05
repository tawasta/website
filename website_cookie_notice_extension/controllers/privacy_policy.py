# -*- coding: utf-8 -*-
# 1. Standard library imports:
import logging

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request
from odoo import api, fields, models, exceptions, _

# 4. Imports from Odoo modules:

class PrivacyPolicy(http.Controller):
	@http.route('/privacy-policy', type='http', website=True, auth="public")
	def page_certificate_verification(self, **kw):
		return request.render('website_cookie_notice_extension.privacy_policy')