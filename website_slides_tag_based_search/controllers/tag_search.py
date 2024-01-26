import logging
import math

import werkzeug

from odoo import http
from odoo.http import request

from odoo.addons.website_slides.controllers.main import WebsiteSlides

_logger = logging.getLogger(__name__)


class WebsiteSlidesTagBasedSearch(WebsiteSlides):
    def _prepare_additional_channel_values(self, values, **kwargs):
        """
        Fetch all the possible slide tags
        """

        values = super(
            WebsiteSlidesTagBasedSearch, self
        )._prepare_additional_channel_values(values, **kwargs)

        fields = ["id", "name"]
        order = "name ASC"

        values["slide_tags"] = request.env["slide.tag"].search_read(
            fields=fields, order=order
        )

        return values

    @http.route(
        [
            '/slides/<model("slide.channel"):channel>/tags/<string:selected_tag_ids>',
            '/slides/<model("slide.channel"):channel>/tags/<string:selected_tag_ids>/page/<int:page>',  # noqa: B950
        ],
        type="http",
        auth="public",
        website=True,
    )
    def channel_multiple_tags(self, channel, page=1, selected_tag_ids="", **kw):

        """
        Based on the channel() function in website_slides.
        """

        _logger.info("channel_multiple_tags reached")
        if not channel.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        domain = super()._get_channel_slides_base_domain(channel)

        pager_url = "/slides/%s" % (channel.id)
        pager_args = {}
        slide_types = dict(
            request.env["slide.slide"]
            ._fields["slide_type"]
            ._description_selection(request.env)
        )

        if selected_tag_ids:
            sanitized_tag_ids = list(map(int, selected_tag_ids.split(",")))
            # The slide must contain all the tags in order to show up in results
            for tag_id in sanitized_tag_ids:
                domain += [("tag_ids.id", "=", tag_id)]
        else:
            sanitized_tag_ids = []

        # sorting criterion
        if channel.channel_type == "documentation":
            default_sorting = (
                "latest"
                if channel.promote_strategy in ["specific", "none", False]
                else channel.promote_strategy
            )
            actual_sorting = default_sorting
        else:
            actual_sorting = "sequence"

        order = request.env["slide.slide"]._order_by_strategy[actual_sorting]
        pager_args["sorting"] = actual_sorting

        slide_count = request.env["slide.slide"].sudo().search_count(domain)

        _logger.info("search count called:")
        _logger.info(slide_count)

        page_count = math.ceil(slide_count / self._slides_per_page)
        pager = request.website.pager(
            url=pager_url,
            total=slide_count,
            page=page,
            step=super()._slides_per_page,
            url_args=pager_args,
            scope=page_count
            if page_count < super()._pager_max_pages
            else super()._pager_max_pages,
        )

        category = None
        uncategorized = None

        values = {
            "channel": channel,
            "main_object": channel,
            "active_tab": kw.get("active_tab", "home"),
            "search_tags": sanitized_tag_ids,
            "slide_types": slide_types,
            "sorting": actual_sorting,
            "rating_avg": channel.rating_avg,
            "rating_count": channel.rating_count,
            "user": request.env.user,
            "pager": pager,
            "is_public_user": request.website.is_public_user(),
            "enable_slide_upload": "enable_slide_upload" in kw,
        }

        if channel.promote_strategy == "specific":
            values["slide_promoted"] = channel.sudo().promoted_slide_id
        else:
            values["slide_promoted"] = (
                request.env["slide.slide"].sudo().search(domain, limit=1, order=order)
            )

        limit_category_data = False
        if channel.channel_type == "documentation":
            if category or uncategorized:
                limit_category_data = super()._slides_per_page
            else:
                limit_category_data = super()._slides_per_category

        values["category_data"] = channel._get_categorized_slides(
            domain,
            order,
            force_void=not category,
            limit=limit_category_data,
            offset=pager["offset"],
        )
        values["channel_progress"] = self._get_channel_progress(
            channel, include_quiz=True
        )

        values = self._prepare_additional_channel_values(values, **kw)
        return request.render("website_slides.course_main", values)
