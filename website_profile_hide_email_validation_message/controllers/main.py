from odoo import http
from odoo.http import request

from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlidesAutoValidate(WebsiteSlides):
    def _auto_validate_email(self):
        """Automatically validate the current user's email if they have karma==0.

        This gives them the standard validation karma gain, which suppresses
        the email validation banner everywhere on the website.
        """
        user = request.env.user
        if request.website.is_public_user():
            return
        if user.karma != 0:
            return
        if not user.email:
            return
        done = request.session.get("validation_email_auto_done")
        if isinstance(done, dict):
            if done.get(user.id):
                return
        elif done:  # legacy boolean True from old sessions
            request.session["validation_email_auto_done"] = {}

        token = user._generate_profile_token(user.id, user.email)
        user._process_profile_validation_token(token, user.email)
        request.session.setdefault("validation_email_auto_done", {})
        request.session["validation_email_auto_done"][user.id] = True
        request.session.modified = True

    @http.route("/slides", type="http", auth="public", website=True, sitemap=True)
    def slides_channel_home(self, **post):
        self._auto_validate_email()
        return super().slides_channel_home(**post)

    @http.route(
        [
            "/slides/all",
            "/slides/all/tag/<string:slug_tags>",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def slides_channel_all(self, slide_category=None, slug_tags=None, my=False, **post):
        self._auto_validate_email()
        return super().slides_channel_all(
            slide_category=slide_category, slug_tags=slug_tags, my=my, **post
        )

    @http.route(
        [
            '/slides/<model("slide.channel"):channel>',
            '/slides/<model("slide.channel"):channel>/page/<int:page>',
            '/slides/<model("slide.channel"):channel>/tag/<model("slide.tag"):tag>',
            '/slides/<model("slide.channel"):channel>/tag/<model("slide.tag"):tag>/page/<int:page>',
            '/slides/<model("slide.channel"):channel>/category/<model("slide.slide"):category>',
            '/slides/<model("slide.channel"):channel>/category/<model("slide.slide"):category>/page/<int:page>',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=WebsiteSlides.sitemap_slide,
    )
    def channel(
        self,
        channel,
        category=None,
        tag=None,
        page=1,
        slide_category=None,
        uncategorized=False,
        sorting=None,
        search=None,
        **kw,
    ):
        self._auto_validate_email()
        return super().channel(
            channel,
            category=category,
            tag=tag,
            page=page,
            slide_category=slide_category,
            uncategorized=uncategorized,
            sorting=sorting,
            search=search,
            **kw,
        )

    @http.route(
        """/slides/slide/<model("slide.slide"):slide>""",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def slide_view(self, slide, **kwargs):
        self._auto_validate_email()
        return super().slide_view(slide, **kwargs)
