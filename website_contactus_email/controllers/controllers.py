# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteContactusEmail(http.Controller):
#     @http.route('/website_contactus_email/website_contactus_email/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_contactus_email/website_contactus_email/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_contactus_email.listing', {
#             'root': '/website_contactus_email/website_contactus_email',
#             'objects': http.request.env['website_contactus_email.website_contactus_email'].search([]),
#         })

#     @http.route('/website_contactus_email/website_contactus_email/objects/<model("website_contactus_email.website_contactus_email"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_contactus_email.object', {
#             'object': obj
#         })