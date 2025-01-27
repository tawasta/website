from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.web import Home as home


class SocietyHome(home):
    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(SocietyHome, self).web_login(redirect=redirect, *args, **kw)
        # MFA: Check pre_uid if half way authed
        if (
            not redirect
            and request.params["login_success"]
            and not request.session.get("pre_uid")
        ):
            if (
                request.website.sudo().landing_page_group_text
                or request.website.sudo().landing_page
            ):
                get_param = request.env["ir.config_parameter"].sudo().get_param
                group_param = get_param("group.landing.page")
                is_in_group = (
                    request.env["res.groups"]
                    .sudo()
                    .search([("id", "=", group_param), ("users", "in", request.uid)])
                )
                if is_in_group and request.website.sudo().landing_page_group_text:
                    redirect = request.website.sudo().landing_page_group_text
                else:
                    redirect = request.website.sudo().landing_page

                return request.redirect(redirect)

        return response

    def _login_redirect(self, uid, redirect=None):
        res = super()._login_redirect(uid, redirect)
        if (
            request.website.sudo().landing_page_group_text
            or request.website.sudo().landing_page
        ):
            if redirect:
                return redirect
            elif (
                request.website.sudo().landing_page_group_text
                or request.website.sudo().landing_page
            ):
                get_param = request.env["ir.config_parameter"].sudo().get_param
                group_param = get_param("group.landing.page")
                is_in_group = (
                    request.env["res.groups"]
                    .sudo()
                    .search([("id", "=", group_param), ("users", "in", request.uid)])
                )
                if is_in_group and request.website.sudo().landing_page_group_text:
                    redirect = request.website.sudo().landing_page_group_text
                else:
                    redirect = request.website.sudo().landing_page

                return redirect
        return res
