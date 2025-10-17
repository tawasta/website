import logging
from datetime import date, datetime, timedelta  # ← timedelta lisätty

from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class PartnerDataPromptController(http.Controller):
    @http.route("/my/data_check", type="json", auth="user", website=True)
    def data_check(self):
        """Palauta datan tarkistus -modalin kentät tilanteen mukaan.

        UUSI LOGIIKKA:
          - Näytä lomake vain, jos data_check_date on None TAI MENNEISYYDESSÄ.
          - Kun käyttäjä on kuitannut/tallentanut, asetetaan data_check_date tulevaisuuteen:
            today + interval_days. Väliaikana lomaketta ei näytetä lainkaan, vaikka
            sääntöjä tulisi lisää tai nykyiset triggaavat.
          - Täystarkistuksessa näytetään sekä ask_on_full_check=True -säännöt
            ETTÄ kaikki condition_domainin läpäisseet säännöt (ask-kentät ensin).
        """
        partner = request.env.user.partner_id
        website = request.env["website"].get_current_website()
        interval_days = website.data_prompt_interval_days or 90

        _logger.info(
            "[data_check] partner_id=%s data_check_date=%s interval_days=%s",
            partner.id,
            partner.data_check_date,
            interval_days,
        )

        # Näytetään modal VAIN, jos tarkistus on erääntynyt (menneisyydessä) tai ei ole tehty
        show_full_check = (
            not partner.data_check_date or partner.data_check_date < date.today()
        )
        if not show_full_check:
            _logger.info("[data_check] check up-to-date → no form to show")
            return False

        # Täystarkistusta varten haetaan säännöt ja muodostetaan kentät
        rules = (
            request.env["res.partner.data.prompt.rule"]
            .sudo()
            .search([("active", "=", True)])
        )
        _logger.info("[data_check] active_rules_count=%s", len(rules))

        all_fields_strict = []  # condition_domain läpäisseet field_datat
        rule_fields = []        # (rule, field_data) -parit

        for rule in rules:
            field_name = rule.field_name.name
            value = getattr(partner, field_name, False)

            field_data = {
                "name": field_name,
                "type": rule.field_type,
                "label": rule.info_text or rule.field_name.field_description,
                "required": rule.required,
                "value": value,
                "options": self._get_field_options(partner, rule)
                if rule.field_type in ["selection", "many2one", "many2many"]
                else [],
            }

            # condition_domain-suodatus (vain täystarkistuksen yhteydessä)
            passed = True
            if rule.condition_domain:
                try:
                    domain = safe_eval(rule.condition_domain)
                    count = (
                        request.env["res.partner"]
                        .sudo()
                        .search_count([("id", "=", partner.id)] + (domain or []))
                    )
                    passed = bool(count)
                    _logger.info(
                        "[data_check] condition_domain check rule=%s passed=%s",
                        rule.name,
                        passed,
                    )
                except Exception as e:
                    _logger.info(
                        "[data_check] Invalid/err domain in rule=%s err=%s",
                        rule.name,
                        e,
                    )
                    passed = False

            if passed:
                all_fields_strict.append(field_data)

            rule_fields.append((rule, field_data))

        # --- YHDISTETTY LISTA ---
        # 1) Nouda ask_on_full_check -kentät
        ask_fields = [fd for r, fd in rule_fields if r.ask_on_full_check]
        # 2) Yhdistä: ask-kentät ensin, sitten kaikki condition_domainin läpäisseet
        combined = ask_fields + all_fields_strict
        # 3) Poista duplikaatit säilyttäen järjestyksen (ask-kentät pysyvät alussa)
        seen = set()
        fields_for_full = []
        for fd in combined:
            name = fd["name"]
            if name not in seen:
                fields_for_full.append(fd)
                seen.add(name)

        # Jos ei ollut ask-kenttiä JA mikään ei läpäissyt condition_domainia,
        # näytetään tyhjä → ei lomaketta (varmistuslogiikka)
        if not fields_for_full:
            _logger.info("[data_check] no fields after merge → no form to show")
            return False

        _logger.info(
            "[data_check] full check → returning fields=%s",
            [f["name"] for f in fields_for_full],
        )
        return request.env["ir.ui.view"]._render_template(
            "partner_data_promt.data_prompt_modal",
            {"fields": fields_for_full},
        )

    @staticmethod
    def _get_field_options(partner, rule):
        """Valintalistat selection/m2o/m2m-kentille."""
        field_name = rule.field_name.name
        field = partner._fields.get(field_name)
        if not field:
            return []
        if field.type == "selection":
            # selection voi olla lista tai callable; palautetaan sellaisenaan
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
        """Päivitä partnerin tiedot lomakkeen postista ja siirrä data_check_date tulevaisuuteen."""
        partner = request.env.user.partner_id
        rules = request.env["res.partner.data.prompt.rule"].sudo().search([])
        allowed_fields = {
            rule.field_name.name: {"type": rule.field_type, "required": rule.required}
            for rule in rules
        }

        # Hae interval, jotta voidaan asettaa seuraavan tarkistuksen eräpäivä
        website = request.env["website"].get_current_website()
        interval_days = website.data_prompt_interval_days or 90
        next_check_date = date.today() + timedelta(days=interval_days)

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
                            # UI:ssa muoto dd.mm.yyyy → tallennetaan YYYY-MM-DD
                            date_obj = datetime.strptime(raw_value, "%d.%m.%Y")
                            values[field_name] = date_obj.strftime("%Y-%m-%d")
                        except ValueError:
                            _logger.warning(
                                "Invalid date format for field %s: %s",
                                field_name,
                                raw_value,
                            )
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

        # Jos tehtiin muutoksia TAI käyttäjä kuittasi tiedot ajantasalle,
        # päivitä aina seuraava tarkistuspäivä tulevaisuuteen
        if values or post.get("confirm_data_is_accurate") == "on":
            values.setdefault("data_check_date", next_check_date)
            values["data_check_date"] = next_check_date
            partner.sudo().write(values)

        referrer = request.httprequest.referrer or "/"
        return request.redirect(referrer)
