# -*- coding: utf-8 -*-

# 1. Standard library imports:
from collections import OrderedDict
# 2. Known third party imports (One per line sorted and splitted in python stdlib):

# 3. Odoo imports (openerp):
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.web import http
from openerp.addons.web.http import request

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in python stdlib):


class website_sale(website_sale):

	# 1. Private attributes

	# 2. Fields declaration	

	# 3. Default methods

	# Save the new fields to partners form
	def checkout_form_save(self, checkout):

		super(website_sale, self).checkout_form_save(checkout)

		cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
		orm_partner = registry.get('res.partner')
		orm_user = registry.get('res.users')
		partner = orm_user.browse(cr, SUPERUSER_ID, request.uid, context).partner_id

		#Partneriin kirjoitus
		partner.staff_count = request.params['staff_count']

		if 'member_privacy' in request.params:
			partner.member_privacy = request.params['member_privacy']
		else:
			partner.member_privacy = False


		if 'steering_member' in request.params:
			partner.steering_member = request.params['steering_member']
		else:
			partner.steering_member = False

	# Get the new fields from partner for to checkout
	def checkout_values(self, data=None):
		cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
		orm_partner = registry.get('res.partner')
		orm_user = registry.get('res.users')
		partner = orm_user.browse(cr, SUPERUSER_ID, request.uid, context).partner_id
		values = super(website_sale, self).checkout_values(data)

		values['checkout']['member_privacy'] = partner.member_privacy
		values['checkout']['staff_count'] = partner.staff_count
		values['checkout']['steering_member'] = partner.steering_member
		self.optional_billing_fields.extend(["staff_count", "member_privacy", "steering_member"])

		staffs = OrderedDict(partner.fields_get(['staff_count'])['staff_count']['selection'])
		values['staffs'] = staffs

		return values


	# 4. Compute and search fields, in the same order that fields declaration

	# 5. Constraints and onchanges

	# 6. CRUD methods

	# 7. Action methods

	# 8. Business methods
