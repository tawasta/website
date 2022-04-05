from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.web import Home as home


class SocietyHome(home):
    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(SocietyHome, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params["login_success"]:
            if (
                request.website.sudo().landing_page_group_text
                or request.website.sudo().landing_page
            ):
                get_param = request.env["ir.config_parameter"].sudo().get_param
                group_param = get_param("group.landing.page")
                is_in_group = (
                    request.env["res.groups"]
                    .sudo()
                    .search(
                        [
                            ("id", "=", group_param),
                            ("users", "in", request.uid),
                        ]
                    )
                )
                if is_in_group and request.website.sudo().landing_page_group_text:
                    redirect = request.website.sudo().landing_page_group_text
                else:
                    redirect = request.website.sudo().landing_page

                return http.redirect_with_hash(redirect)

        return response

    def _login_redirect(self, uid, redirect=None):
        if (
            request.website.sudo().landing_page_group_text
            or request.website.sudo().landing_page
        ):
            get_param = request.env["ir.config_parameter"].sudo().get_param
            group_param = get_param("group.landing.page")
            is_in_group = (
                request.env["res.groups"]
                .sudo()
                .search(
                    [
                        ("id", "=", group_param),
                        ("users", "in", request.uid),
                    ]
                )
            )
            if is_in_group and request.website.sudo().landing_page_group_text:
                redirect = request.website.sudo().landing_page_group_text
            else:
                redirect = request.website.sudo().landing_page

            return redirect
        else:
            return super(SocietyHome, self)._login_redirect(uid, redirect)
