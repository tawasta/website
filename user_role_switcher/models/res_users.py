from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


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
        domain="[('locked_for_allowed_roles', '=', False)]",
    )

    def _check_roles_are_allowed(self, roles):
        """Raise if any of ``roles`` is locked or not marked as allowed.

        Runs as sudo since a non-admin user switching their own role may not
        have read access to ``res.users.role``.
        """
        roles = roles.sudo()
        forbidden = roles.filtered(
            lambda r: r.locked_for_allowed_roles or not r.allow_in_allowed_roles
        )
        if forbidden:
            raise UserError(
                _("The following roles are not allowed to be added or selected: %s")
                % ", ".join(forbidden.mapped("display_name"))
            )

    def _ensure_core_role_is_only(self, role):
        """Make ``base_user_role``'s ``role_line_ids`` hold only ``role``.

        The active role is the single source of truth for the groups
        synced by ``set_groups_from_roles``; any other role previously
        assigned through core is dropped.
        """
        self.ensure_one()
        user = self.sudo()
        user.role_line_ids.filtered(lambda li: li.role_id != role).unlink()
        if role not in user.role_line_ids.role_id:
            self.env["res.users.role.line"].sudo().create(
                {"user_id": user.id, "role_id": role.id}
            )
        user.set_groups_from_roles(force=True)

    def _apply_company_from_allowed_line(self, role):
        """Switch to the company configured on the allowed-role line for ``role``.

        Only applies to the currently logged-in user: writing ``company_id``
        for another user would not affect that user's active session, and
        ``company_ids`` is overridden to contain only the target company to
        avoid an ``_check_company`` violation on the subsequent company switch.
        """
        self.ensure_one()
        if self.id != self.env.user.id:
            return
        line = self.sudo().allowed_role_line_ids.filtered(
            lambda li: li.role_id == role
        )[:1]
        if not line.company_id:
            return

        target = line.company_id
        user = self.sudo()
        if target not in user.company_ids:
            user.write({"company_ids": [(4, target.id)]})
        user.write({"company_id": target.id, "company_ids": [(6, 0, [target.id])]})

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            roles = user.allowed_role_line_ids.role_id
            if roles:
                user.sudo()._check_roles_are_allowed(roles)
            if user.current_role_id:
                user._check_roles_are_allowed(user.current_role_id)
                if user.current_role_id not in roles:
                    raise UserError(
                        _("Active role '%s' must be one of the user's allowed roles.")
                        % user.current_role_id.display_name
                    )
                user._ensure_core_role_is_only(user.current_role_id)
                user._apply_company_from_allowed_line(user.current_role_id)
        return users

    def write(self, vals):
        """Validate allowed/current role consistency and sync core on change.

        The consistency check runs after the write against the persisted
        state (covers changes to ``allowed_role_line_ids`` too, not only to
        ``current_role_id``); the core sync only runs when ``current_role_id``
        was part of this write, since it is the only field that should
        trigger a groups/company change.
        """
        role_changed = "current_role_id" in vals
        if role_changed and vals["current_role_id"]:
            self._check_roles_are_allowed(
                self.env["res.users.role"].browse(vals["current_role_id"])
            )

        res = super().write(vals)

        for user in self.sudo():
            allowed_roles = user.allowed_role_line_ids.role_id
            if allowed_roles:
                user._check_roles_are_allowed(allowed_roles)
            if user.current_role_id and user.current_role_id not in allowed_roles:
                raise UserError(
                    _("Active role '%s' must be one of the user's allowed roles.")
                    % user.current_role_id.display_name
                )

        if role_changed:
            for user in self:
                if user.current_role_id:
                    user._ensure_core_role_is_only(user.current_role_id)
                    user._apply_company_from_allowed_line(user.current_role_id)

        return res

    def switch_role(self, role):
        """Set ``role`` as the user's current role and sync core/company.

        :param res.users.role role: role to switch to; must already be one
            of the user's ``allowed_role_line_ids``.
        :raises AccessError: if called for another user, or for the
            superuser.
        :raises UserError: if ``role`` is not one of the user's allowed
            roles.
        """
        self.ensure_one()
        if self.id != self.env.user.id:
            raise AccessError(_("You can only switch your own roles."))
        if self.id == self.env.ref("base.user_root").id:
            raise AccessError(_("Superuser cannot switch roles for security reasons."))

        self._check_roles_are_allowed(role)
        user = self.sudo()
        if role not in user.allowed_role_line_ids.role_id:
            raise UserError(_("Role '%s' is not allowed for this user.") % role.name)

        user.current_role_id = role
        user._ensure_core_role_is_only(role)
        user._apply_company_from_allowed_line(role)
        return True
