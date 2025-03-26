from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    portal_hide_contract_menuitems = fields.Boolean(
        string="Portal: Hide Contract-related menuitems",
        help="Hide 'Contracts' menuitem in portal, and prevent "
        "access to its related pages",
    )
