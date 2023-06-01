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
# 2. Known third party imports:
# 3. Odoo imports:
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MailThread(models.AbstractModel):

    # 1. Private attributes
    _inherit = "mail.thread"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, *args, **kwargs):
        """
        Enable some of the messages to go through to email and block others.
        This is done by using two mail servers:
        1. Default mail server, doesn't allow emails
        2. Smaller priority server, that allows emails to go through

        In this method we check if we should allow it to go into email (certain models)
        and if it is allowed, we set explicitely the mail server (2.)
        and set the notification layout.
        """
        values = kwargs
        msg_model = self._name
        website = self.env["website"].search(
            [("company_id", "=", self.env.ref("base.main_company").id)], limit=1
        )
        if msg_model in website.sudo().message_email_model_ids.mapped("model") \
                and "mail_auto_delete" not in values:
            website = self.env["website"].search(
                [("company_id", "=", self.env.ref("base.main_company").id)], limit=1
            )
            values.update(
                {
                    "mail_server_id": website.sudo().message_email_mail_server_id.id,
                    "email_layout_xmlid": "website_messages_email.website_message_notification",
                    "add_sign": False,
                    "email_from": website.message_email_from,
                }
            )
            if website.message_email_subject:
                values["subject"] = website.message_email_subject

        return super().message_post(*args, **values)
