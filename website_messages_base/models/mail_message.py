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
##############################################################################
# 1. Standard library imports:
import re
import logging
from uuid import uuid4

# 2. Known third party imports:

# 3. Odoo imports:
from odoo import api
from odoo import fields
from odoo import models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


_logger = logging.getLogger(__name__)


class MailMessage(models.Model):

    # 1. Private attributes
    _inherit = "mail.message"

    # 2. Fields declaration
    website_url = fields.Char(
        string="Website URL",
        help="URL on website",
        compute="_compute_website_url",
        store=True,
    )
    website_thread_id = fields.Char(
        string="Website thread ID",
        help="Thread ID to identify message threads",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends("email_from")
    def _compute_website_url(self):
        """
        Get website url with the help of system parameters.
        email_from field is used to trigger with mass_editing
        module this function
        so the urls are calculated (for better performance)
        """
        website_url = str()
        for record in self:
            # Find url format from system parameters
            # which can be find by key
            # unread_messages_format.<model_name>
            rec = self.env["website.message.format"].search(
                [("res_model", "=", record.model)]
            )
            if rec:
                # URL format in system parameters is following this format
                # /<string>/:<name_of_field>
                # We can retrieve the fields and construct the real
                # URL using those
                # For presenting the res_id object's parent in URL
                # format, we are using
                # res_parent_id (not a field that is used on mail.message)
                website_url = rec.url_format
                parts = re.findall(r":\w+", website_url)
                for part in parts:
                    field_name = re.sub(":", "", part)
                    if part == ":res_parent_id":
                        # Special case: get res_id object's parent's id
                        field_value = (
                            self.env[record.model]
                            .sudo()
                            .browse(record.res_id)
                            .project_id.id
                        )
                    else:
                        field_value = getattr(record, field_name)
                    website_url = website_url.replace(part, str(field_value))
            record.website_url = website_url

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        """
        Save thread ID logic

        :param vals: dict:
        :return: super
        """
        msg_model = vals.get("model")
        website = self.env["website"].search([
            ("company_id", "=", self.env.ref("base.main_company").id)
        ], limit=1)
        if msg_model in website.message_thread_model_ids.mapped("model"):
            thread_id = vals.get("website_thread_id")
            if not thread_id:
                thread_id = str(uuid4())
            vals["website_thread_id"] = thread_id
        return super().create(vals)

    def action_message_thread_init(self):
        """ Set thread id for all models that require it """
        website = self.env["website"].search([
            ("company_id", "=", self.env.ref("base.main_company").id)
        ], limit=1)
        messages = self.search([
            ("website_thread_id", "=", False),
            ("model", "in", website.message_thread_model_ids.mapped("model")),
        ])
        for msg in messages:
            msg.website_thread_id = str(uuid4())

    # 7. Action methods

    # 8. Business methods
