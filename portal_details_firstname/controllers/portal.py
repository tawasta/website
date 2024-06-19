from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalDetails(CustomerPortal):
    # Required fields are defined in a list MANDATORY_BILLING_FIELDS
    CustomerPortal.MANDATORY_BILLING_FIELDS.extend(["firstname", "lastname"])
    CustomerPortal.MANDATORY_BILLING_FIELDS.remove("name")
