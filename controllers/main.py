# -*- coding: utf-8 -*-

# 1. Standard library imports:
from collections import OrderedDict
# 2. Known third party imports (One per line sorted and splitted in python stdlib):

# 3. Odoo imports (openerp):
from openerp import fields, SUPERUSER_ID, _
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

		if 'website' in request.params:
			checkout['website'] = request.params['website']

		# Job position
		if 'function' in request.params:
			checkout['function'] = request.params['function']

		if 'businessid' in request.params:
			checkout['businessid'] = request.params['businessid']
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
		
		# Different form types in this dict
		values['form_type'] = {}

		# This function is called when moving from checkout form to confirmation
		# That's why we have to ensure that when we retrieve values from partner,
		# we do not overwrite user typed data
		if not data:
			values['checkout']['function'] = partner.function
			values['checkout']['businessid'] = partner.businessid
			values['checkout']['website'] = partner.website

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

		# Shorter checkout form will be regocnised with this 
		product = request.website.sale_get_order().product_id.product_tmpl_id

		# All the fields written to partner has to be either in mandatory or optional fields
		self.mandatory_billing_fields = ["name", "email", "city", "country_id"]
		self.optional_billing_fields = []

		return values

	# Add businessid validation to checkout forms validate method
	def checkout_form_validate(self, data):
		cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
		
		tmp_partner = registry['res.partner'].browse(cr, SUPERUSER_ID, uid, context=context)
		partner = request.website.sale_get_order(force_create=1, context=context).partner_id

		error = super(website_sale, self).checkout_form_validate(data)

		businessid = request.params['businessid']
		passed = True

		if businessid: 

			if registry['res.partner'].businessid_invalid_format(businessid):
				passed = False
				error['businessid'] = registry['res.partner'].businessid_invalid_format(businessid)
			
			# Is the businessid already in use?

			if passed: 
				try:
					partner.businessid = businessid
				except:
					error['businessid'] = "Already in use"
					pass
				partner.businessid = None
		else:
			request.params['businessid'] = None
		
		return error

	@http.route(['/shop/payment'], type='http', auth="public", website=True)
	def payment(self, **post):
		""" Payment step. This page proposes several payment means based on available
		payment.acquirer. State at this point :

		- a draft sale order with lines; otherwise, clean context / session and
		back to the shop
		- no transaction in context / session, or only a draft one, if the customer
		did go to a payment.acquirer website but closed the tab without
		paying / canceling
		"""
		# cr, uid, context = request.cr, request.uid, request.context
		# payment_obj = request.registry.get('payment.acquirer')
		# sale_order_obj = request.registry.get('sale.order')

		# order = request.website.sale_get_order(context=context)
		# values = {}
		# redirection = self.checkout_redirection(order)
		# if redirection:
		# 	return redirection

		# shipping_partner_id = False
		# if order:
		# 	if order.partner_shipping_id.id:
		# 		shipping_partner_id = order.partner_shipping_id.id
		# 	else:
		# 		shipping_partner_id = order.partner_invoice_id.id

		# values = {
		# 'order': request.registry['sale.order'].browse(cr, SUPERUSER_ID, order.id, context=context)
		# }
		# values['errors'] = sale_order_obj._get_errors(cr, uid, order, context=context)
		# values.update(sale_order_obj._get_website_data(cr, uid, order, context))

		# if not values['errors']:
		# 	acquirer_ids = payment_obj.search(cr, SUPERUSER_ID, [('website_published', '=', True), ('company_id', '=', order.company_id.id)], context=context)
		# 	values['acquirers'] = list(payment_obj.browse(cr, uid, acquirer_ids, context=context))
		#	render_ctx = dict(context, submit_class='btn btn-primary', submit_txt=_('Send'))
		# for acquirer in values['acquirers']:
		# 	acquirer.button = payment_obj.render(
		# 		cr, SUPERUSER_ID, acquirer.id,
		# 		order.name,
		# 		order.amount_total,
		# 		order.pricelist_id.currency_id.id,
		# 		partner_id=shipping_partner_id,
		# 		tx_values={
		# 		'return_url': '/shop/payment/validate',
		# 		},
		# 		context=render_ctx)
				
		# return request.website.render("website_sale.payment", values)

		values = super(website_sale, self).payment()
		return values

	# 4. Compute and search fields, in the same order that fields declaration

	# 5. Constraints and onchanges

	# 6. CRUD methods

	# 7. Action methods

	# 8. Business methods
