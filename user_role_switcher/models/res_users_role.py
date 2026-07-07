from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    allow_in_allowed_roles = fields.Boolean(
        string="Allow adding to Allowed Roles",
        default=False,
        help="If enabled, this role can be selected into a user's Allowed Roles.",
    )

    locked_for_allowed_roles = fields.Boolean(
        string="Locked for Allowed/Current Role",
        default=False,
        help=(
            "If enabled, this role can never be added to Allowed Roles nor set as "
            "Current Role."
        ),
    )

    @api.constrains("allow_in_allowed_roles", "locked_for_allowed_roles")
    def _check_lock_vs_allow(self):
        for role in self:
            if role.locked_for_allowed_roles and role.allow_in_allowed_roles:
                raise UserError(
                    _("Role '%s' is locked and cannot be allowed at the same time.")
                    % role.display_name
                )

    def _check_locked_field_access(self, vals_list):
        if self.env.user.has_group("base.group_system"):
            return
        for vals in vals_list:
            if "locked_for_allowed_roles" in vals:
                raise AccessError(
                    _(
                        "Only system administrators can set 'Locked for "
                        "Allowed/Current Role'."
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        self._check_locked_field_access(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        self._check_locked_field_access([vals])
        return super().write(vals)
