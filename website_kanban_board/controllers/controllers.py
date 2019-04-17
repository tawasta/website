# -*- coding: utf-8 -*-
# 1. Standard library imports:
import logging
import json

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request
from odoo import api, fields, models, tools, exceptions, _

# 4. Imports from Odoo modules:
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.portal.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)

class PortalTeacher(CustomerPortal):


    #Add student's data to account
    @http.route('/my/home/', type='http', auth='user',
                website=True)
    def home(self, **post):

        current_user = http.request.env.user
        active_project = http.request.env['project.task'].sudo().search([])

        active_states = http.request.env['project.task.type'].sudo().search([], order='sequence ASC')

        print(active_states)
        print(active_project)

        values = ({
            'objects': active_project,
            'states': active_states,
        })

        return request.render(
            "website_kanban_board.kanban_board",
            values,
        )