from odoo import http
from odoo.http import request


class AdvertisementController(http.Controller):
    @http.route("/advertisement/<int:ad_id>/increment_view", type="json", auth="public")
    def increment_view(self, ad_id):
        ad = request.env["advertisement.advertisement"].sudo().browse(ad_id)
        ad.increment_view()
        return {"success": True}

    @http.route(
        "/advertisement/<int:ad_id>/increment_click", type="json", auth="public"
    )
    def increment_click(self, ad_id):
        ad = request.env["advertisement.advertisement"].sudo().browse(ad_id)
        ad.increment_click()
        return {"success": True}
