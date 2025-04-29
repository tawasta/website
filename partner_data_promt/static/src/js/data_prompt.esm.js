/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {jsonrpc} from "@web/core/network/rpc_service";

publicWidget.registry.PartnerDataPrompt = publicWidget.Widget.extend({
    selector: "#wrap",

    start: function () {
        this._super.apply(this, arguments);
        this._showPromptIfNeeded();
    },

    _showPromptIfNeeded: function () {
        jsonrpc("/my/data_check", {})
            .then((modalHtml) => {
                if (!modalHtml) return;
                const $modal = $(modalHtml);
                $modal.find(".modal-body > div").removeClass("container");
                $modal.appendTo(document.body);

                const modalInstance = new Modal($modal[0], {
                    backdrop: "static",
                    keyboard: false,
                });
                modalInstance.show();

                // Alustetaan select2
                $modal.on("shown.bs.modal", function () {
                    $modal.find("select.select2").select2({
                        width: "100%",
                        placeholder: "Select an option",
                        dropdownParent: $modal,
                    });

                    // Alustetaan Tempus Dominus datepicker
                    $modal.find('input.datetimepicker-input').each(function () {
                        const element = this;
                        if (typeof tempusDominus !== "undefined") {
                            new tempusDominus.TempusDominus(element, {
                                display: {
                                    components: {
                                        calendar: true,
                                        date: true,
                                        month: true,
                                        year: true,
                                        decades: true,
                                        clock: false,
                                    },
                                    buttons: {
                                        today: true,
                                        clear: true,
                                        close: true,
                                    },
                                    icons: {
                                        time: 'fa fa-clock',
                                        date: 'fa fa-calendar',
                                        up: 'fa fa-arrow-up',
                                        down: 'fa fa-arrow-down',
                                        previous: 'fa fa-chevron-left',
                                        next: 'fa fa-chevron-right',
                                        today: 'fa fa-calendar-check',
                                        clear: 'fa fa-trash',
                                        close: 'fa fa-times',
                                    },
                                    viewMode: 'calendar',
                                    toolbarPlacement: 'bottom',
                                    calendarWeeks: true,
                                },
                                localization: {
                                    format: 'dd.MM.yyyy',
                                },
                            });
                        } else {
                            console.error("Tempus Dominus is not loaded.");
                        }
                    });
                });

                // Lisätään validointi ennen lomakkeen lähetystä
                $modal.find("form").on("submit", function (ev) {
                    let valid = true;
                    const $form = $(this);

                    // Poista aiemmat virheilmoitukset
                    $form.find(".text-danger").remove();
                    $form.find(".is-invalid").removeClass("is-invalid");

                    // Käydään läpi kaikki kentät, joilla on data-required="true"
                    $form
                        .find(
                            "select[data-required='true'], input[data-required='true']"
                        )
                        .each(function () {
                            const $el = $(this);
                            const val = $el.val();
                            const isEmpty =
                                !val || (Array.isArray(val) && val.length === 0);

                            if (isEmpty) {
                                valid = false;
                                $el.addClass("is-invalid");

                                // Virheviesti (näytetään vain jos ei jo ole)
                                if ($el.next(".text-danger").length === 0) {
                                    $el.closest(".form-group").append(
                                        '<div class="text-danger">This field is required.</div>'
                                    );
                                }
                            }
                        });

                    if (!valid) {
                        ev.preventDefault();
                        ev.stopPropagation();

                        const $firstInvalid = $form.find(".is-invalid").first();
                        if ($firstInvalid.length) {
                            // Fokusoi näkyvään valintaan jos select2
                            if ($firstInvalid.hasClass("select2-hidden-accessible")) {
                                $firstInvalid
                                    .next(".select2")
                                    .find(".select2-selection")
                                    .trigger("focus");
                            } else {
                                $firstInvalid.trigger("focus");
                            }
                        }
                    }
                });

                $modal.on("hidden.bs.modal", function () {
                    $modal.remove();
                });
            })
            .catch((err) => {
                console.error("Modal loading failed", err);
            });
    },
});
