from odoo import models

class WebsiteSnippetFilterBlog(models.Model):
    _inherit = "website.snippet.filter"

    def _get_model_max_limit(self, model_name):
        if model_name == "blog.tag":
            return 60
        return super()._get_model_max_limit(model_name)
