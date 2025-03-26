from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    portal_hide_sale_menuitems = fields.Boolean(
        string="Portal: Hide Sale-related menuitems",
        help="Hide 'Quotations' and 'Sale Orders' menuitems in portal, and prevent "
        "access to their related pages",
    )
