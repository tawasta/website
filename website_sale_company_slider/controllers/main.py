# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2018- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################


# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in


class WebsiteSale(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add business_id to saved values
        """
        is_company = all_values.get('is_company', False)
        business_id = all_values.get('business_id', False)
        country_id = checkout.get('country_id', False)
        vat = checkout.get('vat', False)
        country_code = 'FI'
        # Save is_company always, so that private_customer status is updated
        checkout['is_company'] = is_company
        if business_id:
            checkout['business_id'] = business_id
        if country_id:
            # Change VAT-field format to correct vat-format
            # Parse everything else except numbers and add country code in front
            country_code = request.env['res.country'].search([
                ('id', '=', int(checkout.get('country_id')))
            ]).code
        if vat:
            checkout['vat'] = country_code + re.sub('[^0-9]', '', checkout['vat'])
        return super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

    def checkout_form_validate(self, mode, all_form_values, data):
        """
        Change vat to correct format to accept business id format
        """
        country_code = 'FI'
        if data.get('vat'):
            if data.get('country_id'):
                country_code = request.env['res.country'].search([
                    ('id', '=', int(data.get('country_id')))
                ]).code
            data['vat'] = country_code + re.sub('[^0-9]', '', data['vat'])
        res = super(WebsiteSale, self).checkout_form_validate(mode, all_form_values, data)
        if data.get('vat') and data.get('country_id') and country_code == 'FI':
            # Change back to business ID format if country FI
            vat_stripped = re.sub('[^0-9]', '', data['vat'])
            all_form_values.update({
                'vat': vat_stripped[:7] + '-' + vat_stripped[7:]
            })
        return res
