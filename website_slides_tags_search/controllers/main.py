from odoo import http
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class SlidesSearchExtended(WebsiteSlides):
    @http.route()
    def channel(self, *args, **kw):
        response = super(SlidesSearchExtended, self).channel(*args, **kw)

        tags_search = kw.get("tags_search")

        if tags_search:
            tag_ids = request.env["slide.tag"].browse(
                [int(i) for i in tags_search.split(",")]
            )

            domain = [("id", "in", response.qcontext["slides"].ids)]
            for tag in tag_ids:
                # Search tags with AND operator
                domain.append(("tag_ids", "=", tag.id))

            slides = request.env["slide.slide"].search(domain)

            response.qcontext["tag_ids"] = tag_ids
            response.qcontext["slides"] = slides
            response.qcontext["response_template"] = "website_slides.slides_search"

            if response.qcontext.get("category_datas"):
                category_datas = response.qcontext["category_datas"][0]
                category_datas["slides"] = slides
                category_datas["total"] = len(slides)
                response.qcontext["category_datas"] = [category_datas]

        return response
