# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration
    event_sale_orders = fields.One2many(
        'sale.order',
        'partner_id',
        string='Sales Order',
        compute='compute_sale_orders'
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    @api.one
    def compute_sale_orders(self):

        self.event_sale_orders = self.env['sale.order'].search([(
            'partner_id', '=', self.id),
            ('order_line.event_id', '!=', False)])

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
