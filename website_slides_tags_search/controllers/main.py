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
    @http.route(
        [
            '/slides/<model("slide.channel"):channel>',
            '/slides/<model("slide.channel"):channel>/page/<int:page>',
            '/slides/<model("slide.channel"):channel>/tag/<model("slide.tag"):tag>',
            '/slides/<model("slide.channel"):channel>/tag/<model("slide.tag"):tag>/page/<int:page>',
            '/slides/<model("slide.channel"):channel>/category/<model("slide.slide"):category>',
            '/slides/<model("slide.channel"):channel>/category/<model("slide.slide"):category>/page/<int:page>'
        ],
        type='http',
        auth="public",
        website=True)
    # sitemap=sitemap_slide)
    def channel(self,
                channel,
                category=None,
                tag=None,
                page=1,
                slide_type=None,
                uncategorized=False,
                sorting=None,
                search=None,
                search_tags=None,
                **kw):

        response = super(SlidesSearchExtended, self).channel(
            channel,
            category=category,
            tag=tag,
            page=page,
            slide_type=slide_type,
            uncategorized=uncategorized,
            sorting=sorting,
            search=search,
            search_tags=search_tags,
            **kw)

        if search_tags:
            response.qcontext['last_chosen_tags'] = list(search_tags.split(","))
            response = slide_filter(response, search_tags)

        return response
