from odoo import http
from odoo.http import request


class References(http.Controller):
    @http.route("/get_references/", auth="public", type="json", methods=["POST"])
    def all_references(self):
        references = request.env["res.references"].search_read([], ["name", "image"])
        return references
