from odoo import http
from odoo.addons.website_slides.controllers.main import WebsiteSlides


def slide_filter(response, filter_tags):
    # Remove any slides without any given tags
    def tag_filter(slide):
        slides_tags = slide.tag_ids.mapped("name")
        return all(tag in slides_tags for tag in filter_tags)

    response.qcontext['slides'] = list(filter(
        tag_filter,
        list(response.qcontext['slides'])
    ))

    return response


class SlidesSearchExtended(WebsiteSlides):
    @http.route()
    def channel(self, *args, **kw):

        response = super(SlidesSearchExtended, self).channel(*args, **kw)

        search_tags = kw.get('tags_search')
        search = kw.get('search')
        if not search:
            search_tags = None

        if search_tags:
            response.qcontext['last_chosen_tags'] = search_tags
            response = slide_filter(response, search_tags.split(","))

        return response
