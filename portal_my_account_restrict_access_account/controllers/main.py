import logging

from odoo import http
from odoo.http import request

from odoo.addons.account.controllers.portal import PortalAccount

_logger = logging.getLogger(__name__)


class CustomerPortalRestrictedMyAccount(PortalAccount):
    def _check_invoicing_menuitems_hidden(self, partner):
        """Check if the partner is configured to be allowed to view invoices or not"""
        return partner.portal_hide_invoicing_menuitems

    @http.route()
    def portal_my_invoices(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw
    ):
        """Invoices and Bills link via my documents page"""
        partner = request.env.user.partner_id

        if self._check_invoicing_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(CustomerPortalRestrictedMyAccount, self).portal_my_invoices(
                page=page,
                date_begin=date_begin,
                date_end=date_end,
                sortby=sortby,
                filterby=filterby,
                **kw
            )

    @http.route()
    def portal_my_invoice_detail(
        self, invoice_id, access_token=None, report_type=None, download=False, **kw
    ):
        """Individual invoice"""

        partner = request.env.user.partner_id

        if self._check_invoicing_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(
                CustomerPortalRestrictedMyAccount, self
            ).portal_my_invoice_detail(
                invoice_id=invoice_id,
                access_token=access_token,
                report_type=report_type,
                download=download,
                **kw
            )
