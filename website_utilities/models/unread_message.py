# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class UnreadMessage(models.Model):

    # 1. Private attributes
    _name = 'unread.message'

    _sql_constraints = [
        ('res_model', 'unique(res_model)', _('This model already has a format.'))
    ]

    # 2. Fields declaration
    res_model = fields.Many2one(
        'ir.model',
        string='Resources model',
        help='For what model the format is valid',
        required=True,
    )
    url_format = fields.Char(
        string='URL format of the model',
        help='This field defines the URL format for model',
        required=True,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
