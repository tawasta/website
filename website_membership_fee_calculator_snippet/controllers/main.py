import logging

from odoo import http

_logger = logging.getLogger(__name__)


class MembershipFeeCalculatorController(http.Controller):
    @http.route(
        "/website_membership_fee_calculator/calculate",
        type="json",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def calculate_website_membership_fee(self, fee_basis=0, **kwargs):
        """
        Override this function with your relevant fee calculation logic.
        """

        calculated_fee = "n/a"

        return {"fee": calculated_fee}
