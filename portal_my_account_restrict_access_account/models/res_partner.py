from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    portal_hide_invoicing_menuitems = fields.Boolean(
        string="Portal: Hide Invoicing-related menuitems",
        help="Hide 'Invoices and Bills' menuitem in portal, and prevent "
        "access to its related pages",
    )
