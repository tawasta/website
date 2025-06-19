from odoo import http
import inspect
import logging

_logger = logging.getLogger(__name__)

class DebugLoginInspect(http.Controller):
    @http.route('/debug/login_overrides', type='http', auth='user')
    def debug_login_overrides(self, **kw):
        from odoo.addons.portal.controllers.web import Home as PortalHome
        output = ["== DEBUG LOGIN METHOD OVERRIDES =="]

        methods_to_check = {
            'web_login': getattr(PortalHome, 'web_login', None),
            '_login_redirect': getattr(PortalHome, '_login_redirect', None),
        }

        for method_name, base_method in methods_to_check.items():
            output.append(f"\n-- Checking overrides for: {method_name} --")
            for cls in http.Controller.__subclasses__():
                subclass_method = getattr(cls, method_name, None)
                if subclass_method and subclass_method != base_method:
                    try:
                        file = inspect.getsourcefile(subclass_method)
                        lines, lineno = inspect.getsourcelines(subclass_method)
                        output.append(
                            f"[OVERRIDE] {cls.__name__}.{method_name} at {file}:{lineno}"
                        )
                        output.append("".join(lines[:6]) + "...")
                    except Exception as e:
                        output.append(
                            f"[OVERRIDE] {cls.__name__}.{method_name}: failed to inspect: {e}"
                        )
            output.append("-" * 50)

        return "<pre>{}</pre>".format("\n".join(output))
