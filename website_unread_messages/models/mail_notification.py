##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
import datetime
import logging

# 3. Odoo imports:
from odoo import api, models

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


_logger = logging.getLogger(__name__)


class MailNotification(models.Model):

    # 1. Private attributes
    _inherit = "mail.notification"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model_create_multi
    def create(self, vals_list):
        """Odoo inbox + email notification if sysparam True"""
        email_notification = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_unread_messages.email_notification", False)
        )
        if email_notification:
            for vals in vals_list:
                message = self.env["mail.message"].browse(vals["mail_message_id"])
                just_sent = (
                    datetime.datetime.now() - message.create_date
                ) < datetime.timedelta(seconds=1)
                if (
                    vals["notification_type"] == "email"
                    and vals.get("is_read")
                    and just_sent
                ):
                    vals["is_read"] = False
        return super().create(vals_list)

    def write(self, vals):
        """Odoo inbox + email notification if sysparam True"""
        email_notification = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_unread_messages.email_notification", False)
        )
        if email_notification:
            for rec in self:
                just_sent = (
                    datetime.datetime.now() - rec.mail_message_id.create_date
                ) < datetime.timedelta(seconds=1)
                if (
                    rec.notification_type == "email"
                    and vals.get("is_read")
                    and just_sent
                ):
                    vals["is_read"] = False
        return super().write(vals)

    # 7. Action methods

    # 8. Business methods
