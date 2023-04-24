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
import logging

from odoo import api
from odoo import fields
from odoo import models

# 2. Known third party imports:
# 3. Odoo imports (openerp):

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):

    # 1. Private attributes
    _inherit = "res.config.settings"

    # 2. Fields declaration
    message_email_model_ids = fields.Many2many(
        related="website_id.message_email_model_ids",
        string="Email message models",
        help="Which models are taken into account when sending emails",
        readonly=False,
    )
    message_email_mail_server_id = fields.Many2one(
        related="website_id.message_email_mail_server_id",
        string="Website message mail server",
        help="Which mail server is used for website message emails",
        readonly=False,
    )
    message_email_from = fields.Char(
        related="website_id.message_email_from",
        string="Sender of emails",
        help="Which email address is used for sending the emails",
        readonly=False,
    )
    message_email_subject = fields.Char(
        related="website_id.message_email_subject",
        string="Email subject",
        help="Use static subject for emails",
        readonly=False,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def get_values(self):
        return super(ResConfigSettings, self).get_values()

    # 7. Action methods

    # 8. Business methods
