from odoo import fields, models


class ResUsersAllowedRoleLine(models.Model):
    _name = "res.users.allowed.role.line"
    _description = "Allowed Role per User (with Company)"
    _rec_name = "role_id"
    _order = "id"

    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        ondelete="cascade",
        index=True,
    )
    role_id = fields.Many2one(
        "res.users.role",
        string="Role",
        required=True,
        domain="[('locked_for_allowed_roles','=',False), ('allow_in_allowed_roles','=',True)]",
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        help="Optional user-specific company to activate when this role is selected.",
    )

    _sql_constraints = [
        (
            "user_role_unique",
            "unique(user_id, role_id)",
            "Role already added for this user.",
        ),
    ]
