from odoo import _, models


class WebsiteSnippetFilter(models.Model):
    _inherit = "website.snippet.filter"

    def _get_hardcoded_sample(self, model):
        samples = super()._get_hardcoded_sample(model)

        if model._name == "res.references":
            data = [
                {
                    "name": _("Reference 1"),
                    "description": _("A short reference description."),
                    "link": "#",
                },
                {
                    "name": _("Reference 2"),
                    "description": _("A short reference description."),
                    "link": "#",
                },
                {
                    "name": _("Reference 3"),
                    "description": _("A short reference description."),
                    "link": "#",
                },
            ]

            merged = []
            for index in range(0, max(len(samples), len(data))):
                merged.append({
                    **samples[index % len(samples)],
                    **data[index % len(data)],
                })
            samples = merged

        return samples