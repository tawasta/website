import logging
from ast import literal_eval

from odoo import _, api, models
from odoo.exceptions import MissingError, ValidationError
from odoo.osv import expression

import inspect
from functools import partial

_logger = logging.getLogger(__name__)


class WebsiteSnippetFilter(models.Model):
    _inherit = "website.snippet.filter"

    @api.constrains("limit")
    def _check_limit(self):
        """Mallikohtainen limit-tarkistus."""
        for record in self:
            model_name = (
                record.filter_id.model_id if record.filter_id else record.model_name
            )
            max_limit = record._get_model_max_limit(model_name)
            if not (1 <= record.limit <= max_limit):
                raise ValidationError(
                    _("The limit for model '%(model)s' must be between 1 and %(max)d.")
                    % {
                        "model": model_name or "unknown",
                        "max": max_limit,
                    }
                )

    def _get_model_max_limit(self, model_name):
        return 16

    def _prepare_values(self, limit=None, search_domain=None):
        self.ensure_one()
        model_name = self.filter_id.model_id if self.filter_id else self.model_name
        max_limit = self._get_model_max_limit(model_name)
        max_limit = max(self.limit, max_limit)
        limit = limit and min(limit, max_limit) or max_limit

        if self.filter_id:
            filter_sudo = self.filter_id.sudo()
            domain = filter_sudo._get_eval_domain()
            domain = self.get_additional_domain(filter_sudo.model_id, domain)

            if search_domain:
                domain = expression.AND([domain, search_domain])

            try:
                records = self._search_records(
                    model_name=filter_sudo.model_id,
                    domain=domain,
                    context=literal_eval(filter_sudo.context),
                    sort=literal_eval(filter_sudo.sort),
                    limit=limit,
                )
                return self._filter_records_to_values(records)

            except MissingError:
                _logger.warning(
                    "The provided domain '%s' in 'ir.filters' generated MissingError in '%s'",
                    domain, self._name
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
                    .run() or []
                )
            except MissingError:
                _logger.warning(
                    "The provided domain '%s' in 'ir.actions.server' generated MissingError in '%s'",
                    search_domain, self._name
                )
                return []

    def _search_records(self, model_name, domain, context, sort, limit):
        return (
            self.env[model_name]
            .sudo(False)
            .with_context(**context)
            .search(
                domain,
                order=",".join(sort) if sort else None,
                limit=limit,
            )
        )

    def get_additional_domain(self, model_name, base_domain):
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

    def rule_is_enumerable(self, rule):
        """Checks that it is possible to generate sensible GET queries for
           a given rule (if the endpoint matches its own requirements)."""
        endpoint = getattr(rule, "endpoint", None)
        _logger.debug(
            "Checking rule_is_enumerable for rule=%r, endpoint=%r (%s)",
            getattr(rule, "rule", None), endpoint, type(endpoint)
        )

        # Gather routing properties
        try:
            methods = endpoint.routing.get('methods') or ['GET']
        except AttributeError as e:
            _logger.exception(
                "Missing 'routing' or 'methods' on endpoint=%r for rule=%r",
                endpoint, getattr(rule, "rule", None)
            )
            return False

        converters = list(getattr(rule, "_converters", {}).values())

        if not (
            'GET' in methods
            and endpoint.routing.get('type') == 'http'
            and endpoint.routing.get('auth') in ('none', 'public')
            and endpoint.routing.get('website', False)
            and all(hasattr(converter, 'generate') for converter in converters)
        ):
            _logger.debug(
                "Exiting early as rule/endpoint did not pass basic GET/http/auth/website checks"
            )
            return False

        # Finally check the endpoint's signature
        try:
            func = endpoint.func if isinstance(endpoint, partial) else endpoint.original_endpoint
            sign = inspect.signature(func)
        except Exception as e:
            _logger.exception(
                "Error inspecting endpoint in rule_is_enumerable. Rule=%r endpoint=%r error=%s",
                getattr(rule, "rule", None), endpoint, str(e)
            )
            return False

        params = list(sign.parameters.values())[1:]  # skip self
        supported_kinds = (inspect.Parameter.POSITIONAL_ONLY,
                           inspect.Parameter.POSITIONAL_OR_KEYWORD)

        result = all(
            p.name in rule._converters
            for p in params
            if p.kind in supported_kinds and p.default is inspect.Parameter.empty
        )
        _logger.debug(
            "Rule is enumerable result=%s for rule=%r endpoint=%r",
            result, getattr(rule, "rule", None), endpoint
        )
        return result
