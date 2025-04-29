from odoo import http, _
from odoo.http import request
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class PartnerDataPromptController(http.Controller):
    @http.route("/my/data_check", type="json", auth="user", website=True)
    def data_check(self):
        partner = request.env.user.partner_id
        rules = request.env["res.partner.data.prompt.rule"].sudo().search([('active', '=', True)])

        fields_to_ask = []
        field_data = []

        for rule in rules:
            field_value = getattr(partner, rule.field_name.name, False)
            if field_value:
                continue
            if rule.condition_domain:
                try:
                    domain = eval(rule.condition_domain)
                except Exception as e:
                    _logger.error("Invalid domain in rule %s: %s", rule.name, e)
                    continue
                if not request.env["res.partner"].search_count(
                    [("id", "=", partner.id)] + domain
                ):
                    continue

            fields_to_ask.append(rule.field_name)
            field_data.append(
                {
                    "name": rule.field_name.name,
                    "type": rule.field_type,
                    "label": rule.info_text or rule.field_name.field_description,
                    "required": rule.required,
                    "options": self._get_field_options(partner, rule)
                    if rule.field_type in ["selection", "many2one", "many2many"]
                    else [],
                }
            )
            _logger.info(field_data)

        if fields_to_ask:
            return request.env["ir.ui.view"]._render_template(
                "partner_data_promt.data_prompt_modal", {"fields": field_data}
            )
        return False

    @staticmethod
    def _get_field_options(partner, rule):
        field_name = rule.field_name.name
        field = partner._fields.get(field_name)
        if not field:
            return []
        if field.type == "selection":
            return field.selection
        elif field.type in ["many2one", "many2many"]:
            comodel = field.comodel_name
            records = request.env[comodel].sudo().search([], limit=100)
            return [(r.id, r.display_name) for r in records]
        return []

    @http.route(
        "/my/data_update", type="http", auth="user", methods=["POST"], website=True
    )
    def data_update(self, **post):
        partner = request.env.user.partner_id

        rules = request.env["res.partner.data.prompt.rule"].sudo().search([])
        allowed_fields = {rule.field_name.name: {"type": rule.field_type, "required": rule.required} for rule in rules}

        values = {}
        for field_name, field_info in allowed_fields.items():
            if field_name not in post:
                continue

            field_type = field_info["type"]
            is_required = field_info["required"]
            raw_value = post.get(field_name)

            # Jos kenttä on tyhjä ja EI ole required -> älä tallenna mitään
            if not raw_value and not is_required:
                continue

            try:
                if field_type == "many2one":
                    values[field_name] = int(raw_value) if raw_value else False
                elif field_type == "integer":
                    values[field_name] = int(raw_value) if raw_value else False
                elif field_type == "many2many":
                    raw_list = request.httprequest.form.getlist(field_name)
                    if raw_list:
                        values[field_name] = [(6, 0, [int(x) for x in raw_list])]
                    else:
                        values[field_name] = [(5, 0, 0)]
                elif field_type == "date":
                    if raw_value:
                        try:
                            date_obj = datetime.strptime(raw_value, "%d.%m.%Y")
                            values[field_name] = date_obj.strftime("%Y-%m-%d")
                        except ValueError:
                            _logger.warning("Invalid date format for field %s: %s", field_name, raw_value)
                            values[field_name] = False
                    else:
                        if is_required:
                            values[field_name] = False
                        else:
                            continue  # Optional date, tyhjä -> ei tallenneta
                else:
                    values[field_name] = raw_value
            except Exception as e:
                _logger.warning("Error processing field %s: %s", field_name, e)

        if values:
            _logger.info("Updating partner fields: %s", values)
            partner.sudo().write(values)

        return request.redirect("/")

