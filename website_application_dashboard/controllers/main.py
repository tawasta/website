import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ApplicationDashboardController(http.Controller):
    @http.route(
        [
            "/dashboard",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def dashboard(self, **post):
        """
        Render dashboard page


        {
            <category_id>: [app_user, ...],
            <category_id>: [app_user, ...],
        }
        """
        categories = request.env["dashboard.app.category"].search([])
        apps = request.env["dashboard.app.user"].get_user_apps(request.env.user.id)
        category_data = {}
        for categ in categories:
            category_data[categ.id] = apps.filtered(
                lambda r, categ=categ: r.application_id.category_id.id == categ.id
            )

        render_values = {
            "no_breadcrumbs": True,
            "categories": categories,
            "category_data": category_data,
        }
        return request.render(
            "website_application_dashboard.application_dashboard",
            render_values,
        )

    @http.route(
        [
            "/dashboard/save",
        ],
        type="json",
        auth="user",
    )
    def dashboard_save(self, data, **post):
        """Save dashboard page - positions, visibility and delete own apps"""
        current_user = request.env.user
        categ_id = request.env.ref(
            "website_application_dashboard.dashboard_app_category_personal"
        ).id
        for app_id in data:
            sequence = data.get(app_id).get("position")
            hidden = data.get(app_id).get("hidden")
            removed = data.get(app_id).get("removed")
            user_data = request.env["dashboard.app.user"].browse(int(app_id))
            if user_data:
                app = user_data.application_id
                if (
                    removed
                    and app.user_id.id == current_user.id
                    and app.category_id.id == categ_id
                ):
                    # Check that user created application, then unlink data
                    user_data.unlink()
                    app.sudo().unlink()
                    continue

                user_data.write(
                    {
                        "sequence": sequence,
                        "visible": not hidden,
                    }
                )

    @http.route(
        [
            "/dashboard/create",
        ],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def dashboard_create(self, **post):
        """Create new application"""
        current_user = request.env.user
        if post:
            name = post.get("name")
            url = post.get("url")
            position_before = int(post.get("position_before"))
            categ_id = request.env.ref(
                "website_application_dashboard.dashboard_app_category_personal"
            ).id
            # Take category cards, set new positions
            user_cards = request.env["dashboard.app.user"].search(
                [
                    ("application_id.category_id", "=", categ_id),
                    ("user_id", "=", current_user.id),
                ]
            )
            pos = 1
            create_card_pos = 0
            for card in user_cards:
                if card.application_id.id == position_before:
                    create_card_pos = pos
                    pos += 1

                if create_card_pos != 0:
                    card.sequence = pos
                pos += 1

            new_card = (
                request.env["dashboard.app"]
                .sudo()
                .create(
                    {
                        "name": name,
                        "url": url,
                        "user_id": request.env.uid,
                        "category_id": categ_id,
                    }
                )
            )
            if create_card_pos == 0:
                create_card_pos = len(user_cards)

            request.env["dashboard.app.user"].create(
                {
                    "application_id": new_card.id,
                    "user_id": current_user.id,
                    "sequence": create_card_pos,
                }
            )
        return request.redirect("/dashboard")
