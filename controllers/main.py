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

		if 'staff_count' in request.params:

			checkout['staff_count'] = request.params['staff_count']

		if 'member_privacy' in request.params:
			checkout['member_privacy'] = request.params['member_privacy']
		
		if 'steering_member' in request.params:
			checkout['steering_member'] = request.params['steering_member']

		if 'reason1' in request.params:
			checkout['reason1'] = request.params['reason1']

		if 'reason2' in request.params:
			checkout['reason2'] = request.params['reason2']
		
		if 'reason3' in request.params:
			checkout['reason3'] = request.params['reason3']

		if 'other_reason' in request.params:
			checkout['other_reason'] = request.params['other_reason']

		if 'website' in request.params:
			checkout['website'] = request.params['website']

		# Job position
		if 'function' in request.params:
			checkout['function'] = request.params['function']

		if 'businessid' in request.params:
			checkout['businessid'] = request.params['businessid']
			del checkout['vat'] 
			checkout['is_company'] = True
			checkout['businessid_shown'] = True
			checkout['vatnumber_shown'] = True

		super(website_sale, self).checkout_form_save(checkout)


	# Get the new fields from partner for to checkout
	def checkout_values(self, data=None):
		cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
		orm_partner = registry.get('res.partner')
		orm_user = registry.get('res.users')
		partner = orm_user.browse(cr, SUPERUSER_ID, request.uid, context).partner_id
		values = super(website_sale, self).checkout_values(data)
		
		# This function is called when moving from checkout form to confirmation
		# That's why we have to ensure that when we retrieve values from partner,
		# we do not overwrite user typed data
		if not data:
			values['checkout']['function'] = partner.function
			values['checkout']['staff_count'] = partner.staff_count
			values['checkout']['businessid'] = partner.businessid
			values['checkout']['website'] = partner.website
			values['checkout']['member_privacy'] = partner.member_privacy
			values['checkout']['steering_member'] = partner.steering_member
			values['checkout']['reason1'] = partner.reason1
			values['checkout']['reason2'] = partner.reason2
			values['checkout']['reason3'] = partner.reason3
			values['checkout']['reason4'] = partner.reason4

			# Update checkout when moving backwards so the fills don't disappear
			if request.uid != request.website.user_id.id:

				values['checkout'].update( self.checkout_parse("billing", partner) )
				shipping_ids = orm_partner.search(cr, SUPERUSER_ID, [("parent_id", "=", partner.id), ('type', "=", 'delivery')], context=context)
			else:
				order = request.website.sale_get_order(force_create=1, context=context)
				if order.partner_id:

					domain = [("partner_id", "=", order.partner_id.id)]
					user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID, domain, context=dict(context or {}, active_test=False))
					if not user_ids or request.website.user_id.id not in user_ids:

						values['checkout'].update( self.checkout_parse("billing", order.partner_id) )

		form_type = request.website.sale_get_order().product_id.id

		self.mandatory_billing_fields = ["name", "email", "city", "country_id"]

    	# Shorter form bind to id (Product variants URL id)
		if form_type == 6:
			values['checkout']['form_type'] = "hidden"
			values['checkout']['show_check'] = ""
			self.optional_billing_fields.extend(["reason1", "reason2", "reason3", "reason4", "other_reason"])
		else:
			values['checkout']['form_type'] = ""
			values['checkout']['show_check'] = "hidden"
			self.mandatory_billing_fields.extend(["street2", "street", "zip", "phone", "email", "function", "agreed_box"])
			self.optional_billing_fields.extend(["staff_count", 
				"member_privacy", "steering_member", "website", 
				"businessid", "is_company", "businessid_shown", "vatnumber_shown"])

		staffs = OrderedDict(partner.fields_get(['staff_count'])['staff_count']['selection'])
		values['staffs'] = staffs

		return values

	# Add businessid validation to checkout forms validate method
	def checkout_form_validate(self, data):
		cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

		error = super(website_sale, self).checkout_form_validate(data)

		businessid = data.get('businessid')

		if businessid and registry['res.partner'].businessid_invalid_format(businessid):
			error['businessid'] = registry['res.partner'].businessid_invalid_format(businessid)

		return error

	# 4. Compute and search fields, in the same order that fields declaration

	# 5. Constraints and onchanges

	# 6. CRUD methods

	# 7. Action methods

	# 8. Business methods
