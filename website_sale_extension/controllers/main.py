# -*- coding: utf-8 -*-

# 1. Standard library imports:
from collections import OrderedDict
# 2. Known third party imports (One per line sorted and splitted in python
# stdlib):

# 3. Odoo imports (openerp):
from openerp import fields, SUPERUSER_ID, _
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.web import http
from openerp.addons.web.http import request

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in
# python stdlib):


class website_sale(website_sale):

    # 1. Private attributes

    # 2. Fields declaration

    # 3. Default methods

    # Save the new fields to partners form
    def checkout_form_save(self, checkout):

        order = request.website.sale_get_order(
            force_create=1, context=request.context)

        if 'website' in request.params:
            checkout['website'] = request.params['website']

        # Job position
        if 'function' in request.params:
            checkout['function'] = request.params['function']

        if 'personal_customer' in request.params:
            checkout['personal_customer'] = True

        if 'businessid' in request.params:
            checkout['businessid'] = request.params['businessid']
            checkout['is_company'] = True
            checkout['businessid_shown'] = True
            checkout['vatnumber_shown'] = True

        # If partner already exists (email is in some partner)
        partner_id = http.request.env['res.partner'].sudo().search(
            [('email', '=ilike', request.params['email'])], limit=1)

        if partner_id:
            order.partner_id = partner_id

        super(website_sale, self).checkout_form_save(checkout)

    # Get the new fields from partner for to checkout
    def checkout_values(self, data=None):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        orm_partner = registry.get('res.partner')
        orm_user = registry.get('res.users')
        partner = orm_user.browse(
            cr, SUPERUSER_ID, request.uid, context).partner_id
        values = super(website_sale, self).checkout_values(data)

        # This function is called when moving from checkout form to confirmation
        # That's why we have to ensure that when we retrieve values from partner,
        # we do not overwrite user typed data
        if not data:
            values['checkout']['function'] = partner.function
            values['checkout']['businessid'] = partner.businessid
            values['checkout']['website'] = partner.website
            values['checkout']['personal_customer'] = partner.personal_customer
            # Update checkout when moving backwards so the fills don't
            # disappear
            if request.uid != request.website.user_id.id:

                values['checkout'].update(
                    self.checkout_parse("billing", partner))
                shipping_ids = orm_partner.search(cr, SUPERUSER_ID, [(
                    "parent_id", "=", partner.id), ('type', "=", 'delivery')], context=context)
            else:
                order = request.website.sale_get_order(
                    force_create=1, context=context)
                if order.partner_id:

                    domain = [("partner_id", "=", order.partner_id.id)]
                    user_ids = request.registry['res.users'].search(
                        cr, SUPERUSER_ID, domain, context=dict(context or {}, active_test=False))
                    if not user_ids or request.website.user_id.id not in user_ids:

                        values['checkout'].update(
                            self.checkout_parse("billing", order.partner_id))

        # All the fields written to partner has to be either in mandatory or
        # optional fields
        self.mandatory_billing_fields = [
            "name", "email", "zip", "street", "city", "country_id"
        ]
        self.optional_billing_fields = [
            "phone", "street2", "businessid", "businessid_shown", "is_company", 
            "vatnumber_shown", "website", "function", "personal_customer"
        ]
        
        # Easier to checkout which field are mandatory on website from values
        values['mandatory'] = self.mandatory_billing_fields

        return values

    # Add businessid validation to checkout forms validate method
    def checkout_form_validate(self, data):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        tmp_partner = registry['res.partner'].browse(
            cr, SUPERUSER_ID, uid, context=context)
        partner = request.website.sale_get_order(
            force_create=1, context=context).partner_id

        error = super(website_sale, self).checkout_form_validate(data)

        businessid = request.params['businessid']
        passed = True

        if businessid:

            if registry['res.partner'].businessid_invalid_format(businessid):
                passed = False
                error['businessid'] = registry[
                    'res.partner'].businessid_invalid_format(businessid)

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

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
