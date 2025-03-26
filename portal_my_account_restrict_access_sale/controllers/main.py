import logging

from odoo import http
from odoo.http import request

from odoo.addons.sale.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class CustomerPortalRestrictedMyAccount(CustomerPortal):
    def _check_sale_menuitems_hidden(self, partner):
        """Check if the partner is configured to be allowed to view sales or not"""
        return partner.portal_hide_sale_menuitems

    @http.route()
    def portal_my_quotes(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        """Quotations link via my documents page"""
        partner = request.env.user.partner_id

        if self._check_sale_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(CustomerPortalRestrictedMyAccount, self).portal_my_quotes(
                page, date_begin, date_end, sortby, **kw
            )

    @http.route()
    def portal_my_orders(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        """Sales Orders link via my documents page"""

        partner = request.env.user.partner_id

        if self._check_sale_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(CustomerPortalRestrictedMyAccount, self).portal_my_orders(
                page, date_begin, date_end, sortby, **kw
            )

    @http.route()
    def portal_order_page(
        self,
        order_id,
        report_type=None,
        access_token=None,
        message=False,
        download=False,
        **kw
    ):
        """Individual order/quote"""
        partner = request.env.user.partner_id

        if self._check_sale_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(CustomerPortalRestrictedMyAccount, self).portal_order_page(
                order_id, report_type, access_token, message, download, **kw
            )
