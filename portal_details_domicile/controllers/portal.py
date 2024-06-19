from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalDetails(CustomerPortal):
    # Optional fields are defined in a list OPTIONAL_BILLING_FIELDS
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("domicile")
