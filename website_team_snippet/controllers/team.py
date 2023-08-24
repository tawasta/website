from odoo import http
from odoo.http import request


class Team(http.Controller):
    @http.route("/team/", auth="public", type="json", methods=["POST"])
    def all_team(self):
        members = request.env["res.team"].search_read([], ["name", "image", "professional_title", "description"])
        return members
