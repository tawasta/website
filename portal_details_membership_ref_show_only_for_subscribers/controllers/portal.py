from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalRefForSubscribers(CustomerPortal):
    def _show_partner_ref_in_sidebar(self):
        """Check if user has ongoing subscriptions"""
        ongoing_subscriptions = (
            request.env["sale.subscription.line"]
            .sudo()
            .search(
                [
                    (
                        "sale_subscription_id.partner_id",
                        "=",
                        request.env.user.partner_id.id,
                    ),
                    ("sale_subscription_id.stage_id.type", "=", "in_progress"),
                ]
            )
        )

        return len(ongoing_subscriptions) > 0

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        values["show_partner_ref_in_sidebar"] = self._show_partner_ref_in_sidebar()
        return values
