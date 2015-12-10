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
		order = request.website.sale_get_order(force_create=1, context=context)

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

		if 'reason4' in request.params:
			checkout['reason4'] = request.params['reason4']

		partner_lang = request.lang if request.lang in [lang.code for lang in request.website.language_ids] else None

		billing_info = {'customer': True}
		if partner_lang:
			billing_info['lang'] = partner_lang

		billing_info.update(self.checkout_parse('billing', checkout, True))

		# set partner_id
		partner_id = None
		if request.uid != request.website.user_id.id:
			partner_id = orm_user.browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
		elif order.partner_id:
			user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID,
				[("partner_id", "=", order.partner_id.id)], context=dict(context or {}, active_test=False))
			if not user_ids or request.website.user_id.id not in user_ids:
				partner_id = order.partner_id.id

		# save partner informations
		if partner_id and request.website.partner_id.id != partner_id:
			orm_partner.write(cr, SUPERUSER_ID, [partner_id], billing_info, context=context)
		else:
			# create partner
			partner_id = orm_partner.create(cr, SUPERUSER_ID, billing_info, context=context)
	

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

		values['checkout']['reason1'] = partner.reason1
		values['checkout']['reason2'] = partner.reason2
		values['checkout']['reason3'] = partner.reason3
		values['checkout']['reason4'] = partner.reason4

		form_type = request.website.sale_get_order().product_id.id

		self.mandatory_billing_fields = ["name", "email", "city"]

    	# Shorter form
		if form_type == 66:
			values['checkout']['form_type'] = "hidden"
			values['checkout']['shipping_style'] = "display:none"
			values['checkout']['show_check'] = ""
			self.optional_billing_fields.extend(["reason1", "reason2", "reason3"])
		else:
			values['checkout']['form_type'] = ""
			values['checkout']['shipping_style'] = ""
			values['checkout']['show_check'] = "hidden"
			self.mandatory_billing_fields.extend(["street2"])
			self.optional_billing_fields.extend(["staff_count", "member_privacy", "steering_member", "reason1", "reason2", "reason3"])

		staffs = OrderedDict(partner.fields_get(['staff_count'])['staff_count']['selection'])
		values['staffs'] = staffs

		return values


	# 4. Compute and search fields, in the same order that fields declaration

	# 5. Constraints and onchanges

	# 6. CRUD methods

	# 7. Action methods

	# 8. Business methods
