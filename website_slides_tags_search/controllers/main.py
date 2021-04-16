import werkzeug
from odoo import http, _
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class SlidesSearchExtended(WebsiteSlides):
    @http.route()
    def channel(
        self,
        channel,
        category=None,
        tag=None,
        page=1,
        slide_type=None,
        sorting="creation",
        search=None,
        **kw
    ):
        # Override the whole search function.
        # This seems to be the only viable way to override the search AND pager
        if not channel.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        user = request.env.user
        Slide = request.env["slide.slide"]
        domain = [("channel_id", "=", channel.id)]
        pager_url = "/slides/%s" % (channel.id)
        pager_args = {}
        tags_search = kw.get("tags_search")
        tag_ids = {}

        if search:
            domain += [
                "|",
                "|",
                ("name", "ilike", search),
                ("description", "ilike", search),
                ("index_content", "ilike", search),
            ]
            pager_args["search"] = search
        else:
            if category:
                domain += [("category_id", "=", category.id)]
                pager_url += "/category/%s" % category.id
            if tags_search:
                tag_ids = request.env["slide.tag"].browse(
                    [int(i) for i in tags_search.split(",")]
                )
                tag_list = []
                for tag in tag_ids:
                    tag_list.append(str(tag.id))
                    # Search tags with AND operator
                    domain.append(("tag_ids", "=", tag.id))
                # list into a comma seperated string for url arg
                tag_string = ",".join(tag_list)
                pager_args["tags_search"] = tag_string
            if slide_type:
                domain += [("slide_type", "=", slide_type)]
                # pager_url += "/%s" % slide_type

        if not sorting or sorting not in self._order_by_criterion:
            sorting = "date"
        order = self._order_by_criterion[sorting]
        pager_args["sorting"] = sorting
        pager_count = Slide.search_count(domain)
        pager = request.website.pager(
            url=pager_url,
            total=pager_count,
            page=page,
            step=self._slides_per_page,
            scope=self._slides_per_page,
            url_args=pager_args,
        )
        slides = Slide.search(
            domain, limit=self._slides_per_page, offset=pager["offset"], order=order
        )
        values = {
            "channel": channel,
            "category": category,
            "slides": slides,
            "tag": tag,
            "tag_ids": tag_ids,
            "slide_type": slide_type,
            "sorting": sorting,
            "user": user,
            "pager": pager,
            "is_public_user": user == request.website.user_id,
            "display_channel_settings": not request.httprequest.cookies.get(
                "slides_channel_%s" % (channel.id), False
            )
            and channel.can_see_full,
        }
        if search:
            values["search"] = search
            return request.render("website_slides.slides_search", values)

        # Display uncategorized slides
        if not slide_type and not category:
            category_datas = []
            for category in Slide.read_group(domain, ["category_id"], ["category_id"]):
                category_id, name = category.get("category_id") or (
                    False,
                    _("Uncategorized"),
                )
                category_datas.append(
                    {
                        "id": category_id,
                        "name": name,
                        "total": category["category_id_count"],
                        "slides": Slide.search(
                            category["__domain"], limit=4, offset=0, order=order
                        ),
                    }
                )
            values.update(
                {"category_datas": category_datas,}
            )
        return request.render("website_slides.home", values)
