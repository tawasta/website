import logging
from random import sample

from odoo import models

_logger = logging.getLogger(__name__)


class WebsiteSnippetFilterRandom(models.Model):
    _inherit = "website.snippet.filter"

    def _search_records(self, model_name, domain, context, sort, limit):
        """Yliajaa hakulogiikan advertisement-mallille."""
        if model_name == "advertisement.advertisement":
            all_records = (
                self.env[model_name].sudo(False).with_context(**context).search(domain)
            )
            return sample(list(all_records), k=1) if all_records else all_records

        # Käytetään oletuslogiikkaa muille malleille
        return super()._search_records(model_name, domain, context, sort, limit)
