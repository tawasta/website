from odoo import http
from odoo.addons.website_slides.controllers.main import WebsiteSlides


def slide_filter(response, tags):
    # Remove any slides without any given tags
    def tag_filter(slide):
        in_tag_ids = False
        for tag in slide.tag_ids:
            if tag.name in tags:
                in_tag_ids = True
        return in_tag_ids

    response.qcontext['slides'] = list(filter(
        tag_filter,
        list(response.qcontext['slides'])
    ))

    return response


class SlidesSearchExtended(WebsiteSlides):
    @http.route()
    def channel(self, *args, **kw):

        response = super(SlidesSearchExtended, self).channel(*args, **kw)

        search_tags = kw.get('tags')

        if search_tags:
            response.qcontext['last_chosen_tags'] = list(search_tags.split(","))
            response = slide_filter(response, search_tags)

        return response
