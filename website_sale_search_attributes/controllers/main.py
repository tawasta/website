# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.http import request

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class website_sale(website_sale):

    # 1. Private attributes

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()

        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch),
                    ('attribute_line_ids.value_ids.name', 'ilike', srch)
                ]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        return domain

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
