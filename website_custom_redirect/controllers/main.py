from odoo.addons.web.controllers.utils import is_user_internal
from odoo.addons.web.controllers.home import Home as WebHome


class Home(WebHome):
    def _login_redirect(self, uid, redirect=None):
        if not redirect and redirect != "/my" and not is_user_internal(uid):
            # TODO: configurable redirect
            redirect = "/"
        return super()._login_redirect(uid, redirect=redirect)
