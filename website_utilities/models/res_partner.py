# -*- coding: utf-8 -*-

# 1. Standard library imports:
import logging
import re
import operator

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):

    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.model
    def get_portal_needaction_count(self):
        """
        Compute the number of needaction in portal of the current user.

        1) Search for the models that have set unread_messages_format.<model>
        (these are the "portal messages")
        2) Find messages that have one of these models
        """
        if self.env.user.partner_id:
            enabled_models = self.env['unread.message'].search([])
            model_list = list()
            for rec in enabled_models:
                model_list.append(rec.res_model.model)

            self.env.cr.execute("""
                SELECT count(*) as needaction_count
                FROM mail_message_res_partner_needaction_rel R RIGHT JOIN mail_message M ON (M.id = R.mail_message_id)
                WHERE R.res_partner_id = %s AND M.model IN (%s) """, (self.env.user.partner_id.id, ",".join(map(str, model_list))))
            return (self.env.cr.dictfetchall()[0].get('needaction_count'))
        _logger.error('Call to needaction_count without partner_id')
        return 0

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
