from odoo import http
from odoo.http import request


class PortalRoleSwitcher(http.Controller):
    @http.route(
        ["/portal/switch_role"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def switch_portal_role(self, role_id, **kwargs):
        user = request.env.user.sudo()
        role = request.env["res.users.role"].browse(int(role_id))
        user.switch_role(role)
        return request.redirect(request.httprequest.referrer or "/my")
