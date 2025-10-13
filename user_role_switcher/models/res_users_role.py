from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    allow_in_allowed_roles = fields.Boolean(
        string="Allow adding to Allowed Roles",
        default=False,
        help="If enabled, this role can be selected into a user's Allowed Roles."
    )

    locked_for_allowed_roles = fields.Boolean(
        string="Locked for Allowed/Current Role",
        default=False,
        help="If enabled, this role can never be added to Allowed Roles nor set as Current Role."
    )

    @api.constrains("allow_in_allowed_roles", "locked_for_allowed_roles")
    def _constrains_lock_vs_allow(self):
        """Ensure 'locked' and 'allow' are not enabled at the same time."""
        for rec in self:
            if rec.locked_for_allowed_roles and rec.allow_in_allowed_roles:
                raise UserError(
                    _("Role '%s' is locked and cannot be allowed at the same time.") % rec.display_name
                )

    @api.model
    def create(self, vals):
        """Restrict write access to 'locked_for_allowed_roles' for system admins only."""
        if 'locked_for_allowed_roles' in vals and not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only system administrators can set 'Locked for Allowed/Current Role'."))
        return super().create(vals)

    def write(self, vals):
        """Restrict write access to 'locked_for_allowed_roles' for system admins only."""
        if 'locked_for_allowed_roles' in vals and not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only system administrators can modify 'Locked for Allowed/Current Role'."))
        return super().write(vals)
