import logging

from odoo import http
from odoo.http import request

from odoo.addons.contract.controllers.main import PortalContract

_logger = logging.getLogger(__name__)


class CustomerPortalRestrictedMyAccount(PortalContract):
    def _check_contract_menuitems_hidden(self, partner):
        """Check if the partner is configured to be allowed to view contracts or not"""
        return partner.portal_hide_contract_menuitems

    @http.route()
    def portal_my_contracts(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        """Contracts link via my documents page"""
        partner = request.env.user.partner_id

        if self._check_contract_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(CustomerPortalRestrictedMyAccount, self).portal_my_contracts(
                page=page, date_begin=date_begin, date_end=date_end, sortby=sortby, **kw
            )

    @http.route()
    def portal_my_contract_detail(self, contract_contract_id, access_token=None, **kw):
        """Individual contract"""

        partner = request.env.user.partner_id

        if self._check_contract_menuitems_hidden(partner):
            return request.redirect("/my")
        else:
            return super(
                CustomerPortalRestrictedMyAccount, self
            ).portal_my_contract_detail(
                contract_contract_id=contract_contract_id,
                access_token=access_token,
                **kw
            )
