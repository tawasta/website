from odoo import models
from odoo.exceptions import MissingError
from odoo.osv import expression
from ast import literal_eval
from random import sample
import logging

_logger = logging.getLogger(__name__)


class WebsiteSnippetFilterRandom(models.Model):
    _inherit = "website.snippet.filter"

    def _prepare_values(self, limit=None, search_domain=None):
        self.ensure_one()
        max_limit = max(self.limit, 16)
        limit = limit and min(limit, max_limit) or max_limit

        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()

            if "website_id" in self.env[filter_sudo.model_id]:
                domain = expression.AND(
                    [domain, self.env["website"].get_current_website().website_domain()]
                )
            if "company_id" in self.env[filter_sudo.model_id]:
                website = self.env["website"].get_current_website()
                domain = expression.AND(
                    [domain, [("company_id", "in", [False, website.company_id.id])]]
                )
            if "is_published" in self.env[filter_sudo.model_id]:
                domain = expression.AND([domain, [("is_published", "=", True)]])
            if search_domain:
                domain = expression.AND([domain, search_domain])

            try:
                model_name = filter_sudo.model_id

                # Hae kaikki ilman limit, jos advertisement.advertisement
                if model_name == "advertisement.advertisement":
                    all_records = (
                        self.env[model_name]
                        .sudo(False)
                        .with_context(**literal_eval(filter_sudo.context))
                        .search(domain)
                    )

                    if all_records:
                        records = sample(list(all_records), k=1)  # yksi random
                    else:
                        records = all_records
                else:
                    # Normaali haku rajalla
                    records = (
                        self.env[model_name]
                        .sudo(False)
                        .with_context(**literal_eval(filter_sudo.context))
                        .search(
                            domain,
                            order=",".join(literal_eval(filter_sudo.sort)) or None,
                            limit=limit,
                        )
                    )

                _logger.info("RETURNED RECORDS: %s", records)
                return self._filter_records_to_values(records)

            except MissingError:
                _logger.warning(
                    "The provided domain %s in 'ir.filters' generated a MissingError in '%s'",
                    domain,
                    self._name,
                )
                return []

        elif self.action_server_id:
            try:
                return (
                    self.action_server_id.with_context(
                        dynamic_filter=self,
                        limit=limit,
                        search_domain=search_domain,
                    )
                    .sudo()
                    .run()
                    or []
                )
            except MissingError:
                _logger.warning(
                    "The provided domain %s in 'ir.actions.server' generated a MissingError in '%s'",
                    search_domain,
                    self._name,
                )
                return []
