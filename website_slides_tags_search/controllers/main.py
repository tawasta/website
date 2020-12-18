from odoo import http
from odoo.addons.website_slides.controllers.main import WebsiteSlides


def slide_filter(response, filter_tags):
    # Remove any slides without any given tags
    def tag_filter(slide):
        slides_tags = slide.tag_ids.mapped("name")
        return all(tag in slides_tags for tag in filter_tags)

    slides = list(filter(tag_filter, list(response.qcontext["slides"])))
    response.qcontext["slides"] = slides

    if response.qcontext.get("category_datas"):
        category_datas = response.qcontext["category_datas"][0]
        category_datas["slides"] = slides
        category_datas["total"] = len(slides)
        response.qcontext["category_datas"] = [category_datas]

    return response


class SlidesSearchExtended(WebsiteSlides):
    @http.route()
    def channel(self, *args, **kw):
        response = super(SlidesSearchExtended, self).channel(*args, **kw)

        search_tags = kw.get("tags_search")

        if search_tags:
            response.qcontext["last_chosen_tags"] = search_tags
            response = slide_filter(response, search_tags.split(","))

        return response
