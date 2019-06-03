from odoo import http
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteFilebank(WebsiteSlides):
    @http.route('/filebank', type='http', auth='public', website=True)
    def filebank_index(self, *args, **post):
        # domain = request.website.website_domain()
        channels = request.env['slide.channel']\
            .search([('name', '=like', '% Filebank')], order='sequence, id')
        if not channels:
            return request.render("website_slides.channel_not_found")
        elif len(channels) == 1:
            return request.redirect("/slides/%s" % channels.id)
        values = {
            'channels': channels,
            'user': request.env.user,
            'is_public_user': request.env.user == request.website.user_id
        }
        return request.render('website_filebank.filebank_listing', values)

    @http.route('/slides', type='http', auth="public", website=True)
    def slides_index(self, *args, **post):
        """ Returns a list of available channels: if only one is available,
        redirects directly to its slides
        """
        # domain = request.website.website_domain()
        channels = request.env['slide.channel']\
            .search([('name', 'not like', '% Filebank')], order='sequence, id')
        if not channels:
            return request.render("website_slides.channel_not_found")
        elif len(channels) == 1:
            return request.redirect("/slides/%s" % channels.id)
        return request.render('website_slides.channels', {
            'channels': channels,
            'user': request.env.user,
            'is_public_user': request.env.user == request.website.user_id
        })
