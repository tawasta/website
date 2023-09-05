from odoo import http
from odoo.http import request
import logging


class References(http.Controller):
    @http.route("/get_references/", auth="public", type="json", methods=["POST"])
    def all_references(self):
        references = request.env["res.references"].search_read([], ["name", "image"])
        logging.info("=======REFERENCES===========");
        logging.info(references);
        return references
