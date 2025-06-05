from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    data_check_date = fields.Date(
        string="Data Check Date",
        help="The date when the user last reviewed or updated their information.",
    )


class PartnerDataPromptRule(models.Model):
    _name = "res.partner.data.prompt.rule"
    _description = "Partner Data Prompt Rule"
    _order = "sequence, id"

    name = fields.Char(required=True)
    field_name = fields.Many2one(
        "ir.model.fields",
        string="Field",
        required=True,
        ondelete="cascade",
        domain=[("model", "=", "res.partner"), ("readonly", "=", False)],
        help="Select a field from res.partner to prompt the user for.",
    )
    required = fields.Boolean(default=True)
    condition_domain = fields.Char(
        help="Python domain syntax, e.g. [('is_member','=',True)]"
    )
    info_text = fields.Text(
        string="Prompt Text", help="Explanation shown to user when prompting this field"
    )
    field_type = fields.Char(compute="_compute_field_type", store=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(string="Active")

    @api.depends("field_name")
    def _compute_field_type(self):
        for rule in self:
            rule.field_type = rule.field_name.ttype if rule.field_name else "char"
