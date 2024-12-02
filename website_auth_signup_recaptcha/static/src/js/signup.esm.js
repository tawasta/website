/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignUpForm.include({
    /**
     * Override the `_onSubmit` method to add reCAPTCHA validation
     * while preserving the original functionality.
     */
    _onSubmit: function (ev) {
        // Tarkista reCAPTCHA-vastaus ennen mitään muuta
        var recaptchaResponse = $("#g-recaptcha-response").val();
        if (!recaptchaResponse) {
            // Jos reCAPTCHA ei ole suoritettu, näytä virheilmoitus
            ev.preventDefault(); // Estä lomakkeen oletuslähetys
            this.$("#err").text("Please complete the reCAPTCHA verification.");
            return false;
        }

        // Poista virheilmoitus, jos tarkistus onnistuu
        this.$("#err").text("");
        $("#g-recaptcha-response").remove();

        // Kutsu alkuperäistä toimintoa
        this._super.apply(this, arguments);
    },
});
