from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        result = super().session_info()
        # Same condition as the portal's "Change Role" link (views/user_role.xml)
        result["user_role_switcher_multi_role"] = (
            len(self.env.user.allowed_role_line_ids) > 1
        )
        return result
