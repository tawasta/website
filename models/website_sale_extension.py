# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports (One per line sorted and splitted in python stdlib):

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in python stdlib):


class WebsiteSaleExtension(models.Model):
	
	# 1. Private attributes
	_inherit = 'res.partner'

	# 2. Fields declaration	
	staff_count = fields.Selection([('--', '--'), ('1-9', '1-9'), ('10-19', '10-19'),
									('20-49', '20-49'), ('50-199', '50-199'),
									('200-499', '200-499'), ('500+', '500+')], 
									'Number of Staff')
	# 3. Default methods

	# 4. Compute and search fields, in the same order that fields declaration