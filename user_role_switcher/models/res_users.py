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

    allowed_role_ids = fields.Many2many(
        "res.users.role",
        "res_users_allowed_role_rel",
        "user_id",
        "role_id",
        string="Allowed Roles",
    )
    current_role_id = fields.Many2one("res.users.role", string="Current Role")

    @api.model
    def create(self, vals):
        user = super().create(vals)
        # Jos current_role_id ei ole asetettu ja allowed_role_ids on, luodaan role_line_ids
        if not user.current_role_id and user.allowed_role_ids:
            for role in user.allowed_role_ids:
                # Luo role_line_id vain, jos sitä ei vielä ole
                if not user.role_line_ids.filtered(lambda l: l.role_id == role):
                    self.env["res.users.role.line"].sudo().create(
                        {
                            "user_id": user.id,
                            "role_id": role.id,
                        }
                    )
            # Päivitä ryhmät force=True
            user.set_groups_from_roles(force=True)
        return user

    def switch_role(self, role):
        """Switch active role for user: update current_role_id, role_line_ids, and groups."""
        self.ensure_one()
        # Vain omaa tiliä voi muokata
        if self.id != self.env.user.id:
            raise AccessError(_("You can only switch your own roles."))
        user = self.sudo()

        # Superuser-tarkistus
        if user.id == self.env.ref("base.user_root").id:
            raise AccessError(_("Superuser cannot switch roles for security reasons."))

        # Sallittujen roolien tarkistus
        if role not in user.allowed_role_ids:
            raise UserError(_("Role '%s' is not allowed for this user.") % role.name)

        # Päivitä current_role_id
        user.current_role_id = role

        # Luo valittu rooli jos sitä ei vielä ole
        existing_line = user.role_line_ids.filtered(lambda l: l.role_id == role)
        if not existing_line:
            self.env["res.users.role.line"].sudo().create(
                {
                    "user_id": user.id,
                    "role_id": role.id,
                }
            )

        # Poista kaikki muut role_line_ids paitsi valittu
        lines_to_remove = user.role_line_ids.filtered(lambda l: l.role_id != role)
        if lines_to_remove:
            lines_to_remove.sudo().unlink()

        # Päivitä ryhmät core-logiikan mukaisesti
        user.set_groups_from_roles(force=True)

        # --- Tarkistus: onko käyttäjä sisäinen vai ulkoinen ---
        internal_group = self.env.ref("base.group_user")
        portal_group = self.env.ref("base.group_portal")

        is_internal = internal_group in user.groups_id
        is_portal = portal_group in user.groups_id
        main_company = (
            self.env.ref("base.main_company", raise_if_not_found=False)
            or self.env.company
        )
        if is_internal:
            other_companies = user.company_ids.filtered(
                lambda c: not main_company or c.id != main_company.id
            )
            if other_companies:
                target_company = other_companies[0]
                if user.company_id != target_company:
                    user.sudo().write({"company_id": target_company.id})
        elif is_portal:
            if main_company:
                if user.company_id != main_company:
                    user.sudo().write({"company_id": main_company.id})

        else:
            _logger.warning(
                "User %s does not belong to standard internal or portal groups",
                user.login,
            )

        return True
