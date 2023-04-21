##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
from odoo import fields
from odoo import models

# 2. Known third party imports:
# 3. Odoo imports (openerp):

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Website(models.Model):

    # 1. Private attributes
    _inherit = "website"

    # 2. Fields declaration
    message_email_model_ids = fields.Many2many(
        comodel_name="ir.model",
        string="Email message models",
        help="Which models are taken into account when sending emails",
        relation="message_email_model_rel",
    )
    message_email_mail_server_id = fields.Many2one(
        comodel_name="ir.mail_server",
        string="Website message mail server",
        help="Which mail server is used for website message emails",
    )
    message_email_from = fields.Char(
        string="Sender of emails",
        help="Which email address is used for sending the emails",
    )
    message_email_subject = fields.Char(
        string="Email subject",
        help="Use static subject for emails",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
