import logging
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError

_logger = logging.getLogger(__name__)

FORBIDDEN_GROUPS = [
    "base.group_no_one",
    "base.group_system",
]


class ResUsers(models.Model):
    _inherit = "res.users"

    allowed_role_line_ids = fields.One2many(
        "res.users.allowed.role.line",
        "user_id",
        string="Allowed Roles",
        help="User-specific allowed roles with optional company preference.",
    )

    current_role_id = fields.Many2one(
        "res.users.role",
        string="Current Role",
        domain="[('locked_for_allowed_roles','=',False)]",
    )

    def _check_roles_are_allowed(self, roles):
        """Check that roles are allowed and not locked (executed as sudo)."""
        roles = roles.sudo()
        forbidden = roles.filtered(
            lambda r: r.locked_for_allowed_roles or not r.allow_in_allowed_roles
        )
        if forbidden:
            names = ", ".join(forbidden.mapped("display_name"))
            raise UserError(
                _("The following roles are not allowed to be added or selected: %s") % names
            )

    def _ensure_core_role_is_only(self, role):
        """Ensure core role_line_ids has only the given role, then sync groups."""
        self.ensure_one()
        user = self.sudo()
        user.role_line_ids.filtered(lambda l: l.role_id != role).sudo().unlink()
        if not user.role_line_ids.filtered(lambda l: l.role_id == role):
            self.env["res.users.role.line"].sudo().create(
                {"user_id": user.id, "role_id": role.id}
            )
        user.set_groups_from_roles(force=True)

    def _apply_company_from_allowed_line(self, role):
        """Switch company to the one set on the user's allowed role line, if any."""
        self.ensure_one()
        user = self.sudo()
        line = user.allowed_role_line_ids.filtered(lambda l: l.role_id == role)[:1]
        if not line or not line.company_id:
            return
        target = line.company_id
        if target not in user.company_ids:
            user.write({"company_ids": [(4, target.id)]})
        if user.company_id != target:
            user.write({"company_id": target.id})

    @api.model
    def create(self, vals):
        """Validate allowed lines; only set core when current_role_id is provided."""
        user = super().create(vals)

        roles = user.allowed_role_line_ids.mapped("role_id")
        if roles:
            user.sudo()._check_roles_are_allowed(roles)

        if user.current_role_id:
            self._check_roles_are_allowed(user.current_role_id)
            if user.current_role_id not in roles:
                raise UserError(
                    _("Active role '%s' must be one of the user's allowed roles.")
                    % user.current_role_id.display_name
                )
            user._ensure_core_role_is_only(user.current_role_id)
            user._apply_company_from_allowed_line(user.current_role_id)

        return user

    def write(self, vals):
        """Do NOT sync allowed lines to core. Only touch core when current_role_id changes."""
        roles_to_check = self.env["res.users.role"]

        # Validate new roles referenced in allowed_role_line_ids commands (robust)
        if "allowed_role_line_ids" in vals:
            cmd_list = vals.get("allowed_role_line_ids") or []
            line_model = self.env["res.users.allowed.role.line"]
            for item in cmd_list:
                if not isinstance(item, (list, tuple)) or not item:
                    continue
                cmd = item[0]
                if cmd == 0 and len(item) >= 3 and isinstance(item[2], dict):
                    rid = item[2].get("role_id")
                    if rid:
                        roles_to_check |= self.env["res.users.role"].browse(int(rid))
                elif cmd == 4 and len(item) >= 2:
                    line = line_model.browse(int(item[1]))
                    if line.role_id:
                        roles_to_check |= line.role_id
                elif cmd == 6 and len(item) >= 3:
                    line_ids = item[2] or []
                    lines = line_model.browse([int(x) for x in line_ids])
                    roles_to_check |= lines.mapped("role_id")

        # Validate current role if it's being changed
        new_role = False
        if vals.get("current_role_id"):
            new_role = self.env["res.users.role"].browse(int(vals["current_role_id"]))
            roles_to_check |= new_role

        if roles_to_check:
            self._check_roles_are_allowed(roles_to_check)

        res = super().write(vals)

        # If allowed lines changed, ensure current role is still allowed
        if "allowed_role_line_ids" in vals:
            for user in self:
                if user.current_role_id and user.current_role_id not in user.allowed_role_line_ids.mapped("role_id"):
                    raise UserError(
                        _("Active role '%s' must remain among the user's allowed roles.")
                        % user.current_role_id.display_name
                    )

        # If current role changed, enforce it in core and apply company
        if new_role:
            for user in self:
                if user.current_role_id:
                    if user.current_role_id not in user.allowed_role_line_ids.mapped("role_id"):
                        raise UserError(
                            _("Active role '%s' must be one of the user's allowed roles.")
                            % user.current_role_id.display_name
                        )
                    user._ensure_core_role_is_only(user.current_role_id)
                    user._apply_company_from_allowed_line(user.current_role_id)

        return res

    def switch_role(self, role):
        """Switch the current role using allowed lines; only active role goes to core."""
        self.ensure_one()
        if self.id != self.env.user.id:
            raise AccessError(_("You can only switch your own roles."))

        user = self.sudo()

        if user.id == self.env.ref("base.user_root").id:
            raise AccessError(_("Superuser cannot switch roles for security reasons."))

        self._check_roles_are_allowed(role)

        if role not in user.allowed_role_line_ids.mapped("role_id"):
            raise UserError(_("Role '%s' is not allowed for this user.") % role.name)

        user.current_role_id = role
        user._ensure_core_role_is_only(role)
        user._apply_company_from_allowed_line(role)
        return True
