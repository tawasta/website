from odoo import models
from odoo.exceptions import MissingError
from odoo.osv import expression
from ast import literal_eval
import logging

_logger = logging.getLogger(__name__)


class WebsiteSnippetFilter(models.Model):
    _inherit = "website.snippet.filter"

    def _prepare_values(self, limit=None, search_domain=None):
        """Gets the data and returns it the right format for render."""
        self.ensure_one()

        max_limit = max(self.limit, 16)
        limit = limit and min(limit, max_limit) or max_limit

        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()

            # Käytetään perittävää metodia
            domain = self.get_additional_domain(filter_sudo.model_id, domain)

            if search_domain:
                domain = expression.AND([domain, search_domain])

            try:
                records = (
                    self.env[filter_sudo.model_id]
                    .sudo(False)
                    .with_context(**literal_eval(filter_sudo.context))
                    .search(
                        domain,
                        order=",".join(literal_eval(filter_sudo.sort)) or None,
                        limit=limit,
                    )
                )
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

    def get_additional_domain(self, model_name, base_domain):
        """Return additional domain clauses based on the model."""
        base_domain = self._get_website_domain(model_name, base_domain)
        base_domain = self._get_company_domain(model_name, base_domain)
        base_domain = self._get_is_published_domain(model_name, base_domain)
        return base_domain

    def _get_website_domain(self, model_name, domain):
        if "website_id" in self.env[model_name]:
            return expression.AND(
                [domain, self.env["website"].get_current_website().website_domain()]
            )
        return domain

    def _get_company_domain(self, model_name, domain):
        if "company_id" in self.env[model_name]:
            website = self.env["website"].get_current_website()
            return expression.AND(
                [domain, [("company_id", "in", [False, website.company_id.id])]]
            )
        return domain

    def _get_is_published_domain(self, model_name, domain):
        if "is_published" in self.env[model_name]:
            return expression.AND([domain, [("is_published", "=", True)]])

        return domain

