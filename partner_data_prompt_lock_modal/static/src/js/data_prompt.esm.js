/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PartnerDataPromptLockModal = publicWidget.Widget.extend({
    selector: ".o_portal_wrap",

    start() {
        this._super.apply(this, arguments);
        this._installGuards();
    },

    _installGuards() {
        console.log("Installing partner data prompt modal guards");
        // 1) Estä modalia sulkeutumasta, jos lomake ei ole "valmis"
        $(document).on("hide.bs.modal", "#partnerDataPromptModal", function (ev) {
            const $modal = $(this);
            const isCompleted = $modal.data("partner-data-completed") === true;

            if (!isCompleted) {
                console.log("Blocking partner data prompt modal close");
                // Estä sulkeminen (X-nappi, programmatic close, jne.)
                ev.preventDefault();
                ev.stopImmediatePropagation();
            }
        });

        // 2) Merkitse modal "valmiiksi" vasta kun submit oikeasti menee läpi
        $(document).on("submit", "#partnerDataPromptForm", function (ev) {
            // Tässä vaiheessa kaikki aiemmin rekisteröidyt submit-handlerin pitäisi
            // olla ajettu (ml. alkuperäinen validointi).
            if (ev.isDefaultPrevented && ev.isDefaultPrevented()) {
                // Alkuperäinen validointi blokkaa submitin -> älä merkitse valmiiksi.
                return;
            }

            // Submit on menossa oikeasti läpi -> sallitaan modalille sulkeutuminen
            // (käytännössä selain kuitenkin vaihtaa sivua redirectin takia).
            const $modal = $("#partnerDataPromptModal");
            $modal.data("partner-data-completed", true);
        });
    },
});
