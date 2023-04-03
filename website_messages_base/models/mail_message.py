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
    # Moved from skills_submission_reply
    message_reply_id = fields.Many2one(
        comodel_name="mail.message",
        string="Reply to message",
        help="Message is a reply to this selected message",
        index=True,
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
        if vals.get("message_reply_id"):
            reply = self.env["mail.message"].sudo().browse([vals.get("message_reply_id")])
            thread_id = str(uuid4())
            if reply.website_thread_id:
                vals["website_thread_id"] = reply.website_thread_id
            else:
                vals["website_thread_id"] = thread_id
                reply.website_thread_id = thread_id
        return super().create(vals)

    # 7. Action methods
    def action_calculate_website_thread_id(self):
        """
        This method computes thread IDs for different threads between messages.
        Thread ID is set if:
          1. Message doesn"t reference another message,
          but other message reference the message (starts the thread)

          2. Message references another message

        Thread ID is calculated for the first message in thread and it's submessages
        use the same thread ID.
        """
        website = self.env["website"].search([
            ("company_id", "=", self.env.user.company_id.id)
        ], limit=1)
        no_replies = self.env["mail.message"].sudo().search([
            ("model", "in", website.message_thread_model_ids.mapped("model")),
            ("message_reply_id", "=", False),
        ])
        all_replies = self.env["mail.message"].sudo().search([
            ("model", "in", website.message_thread_model_ids.mapped("model")),
            ("message_reply_id", "!=", False),
        ])
        _logger.info("Calculating thread IDs for {} messages".format(len(all_replies)))
        for message in all_replies:
            if not message.website_thread_id:
                message.website_thread_id = self.compute_thread_id(message)

        _logger.info(
            "Calculating thread IDs for {} messages without replies".format(len(no_replies)))
        for message in no_replies:
            if not message.website_thread_id:
                message.website_thread_id = self.compute_thread_id(message)

    def compute_thread_id(self, message):
        """
        Recursive function to calculate thread IDs

        :param message: mail.message recod
        :return: tuple
        """
        thread_id = str(uuid4())
        if message.message_reply_id:
            thread_id = self.compute_thread_id(message.message_reply_id)

        if not message.website_thread_id:
            message.website_thread_id = thread_id
        return message.website_thread_id

    # 8. Business methods
