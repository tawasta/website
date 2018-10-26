# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re
import operator

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MailMessage(models.Model):

    # 1. Private attributes
    _inherit = 'mail.message'

    # 2. Fields declaration
    website_url = fields.Char(
        string='Website URL',
        help="URL on website",
        compute='_compute_website_url',
        store=True,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends('email_from')
    def _compute_website_url(self):
        """
        Get website url with the help of system parameters.
        email_from field is used to trigger with mass_editing module this function
        so the url's are calculated (for better performance)
        """
        website_url = str()
        for record in self:
            # Find url format from system parameters
            # which can be find by key
            # unread_messages_format.<model_name>
            rec = self.env['unread.message'].search([
                ('res_model', '=', record.model)
            ])
            if rec:
                # URL format in system parameters is following this format
                # /<string>/:<name_of_field>
                # We can retrieve the fields and construct the real URL using those
                # For presenting the res_id object's parent in URL format, we are using
                # res_parent_id (not a field that is used on mail.message)
                website_url = rec.url_format
                parts = re.findall(r':\w+', website_url)
                for part in parts:
                    field_name = re.sub(':', '', part)
                    if part == ':res_parent_id':
                        # Special case: get res_id object's parent's id
                        field_value = self.env[record.model].sudo().browse(record.res_id).project_id.id
                    else:
                        field_value = getattr(record, field_name)
                    website_url = website_url.replace(part, str(field_value))
            record.website_url = website_url


    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
