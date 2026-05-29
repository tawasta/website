from odoo import _, models


class WebsiteSnippetFilter(models.Model):
    _inherit = "website.snippet.filter"

    def _get_hardcoded_sample(self, model):
        if model._name != "res.references":
            return super()._get_hardcoded_sample(model)

        return [
            {
                "name": _("Reference 1"),
                "description": _("A short reference description."),
                "image": b"",
                "link": "#",
                "button_link": "#",
            },
            {
                "name": _("Reference 2"),
                "description": _("A short reference description."),
                "image": b"",
                "link": "#",
                "button_link": "#",
            },
            {
                "name": _("Reference 3"),
                "description": _("A short reference description."),
                "image": b"",
                "link": "#",
                "button_link": "#",
            },
        ]
