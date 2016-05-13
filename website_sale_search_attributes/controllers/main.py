# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports (One per line sorted and splitted in python
# stdlib):

# 3. Odoo imports (openerp):
from openerp.addons.website_sale.controllers.main import website_sale

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in
# python stdlib):


class website_sale(website_sale):

    # 1. Private attributes

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
     def _get_search_domain(self, search, category, attrib_values):
         domain = super(website_sale, self)._get_search_domain(search, category, attrib_values)

         return domain

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
