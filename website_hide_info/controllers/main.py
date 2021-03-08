from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import main


class WebsiteHideInfo(main.Website):
    @http.route("/website/info", type="http", auth="user", website=True)
    def website_info(self):
        super(WebsiteHideInfo, self).website_info()
        return request.render("website.404")
