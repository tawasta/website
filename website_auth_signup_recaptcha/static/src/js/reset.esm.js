/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ResetPasswordForm = publicWidget.Widget.extend({
    selector: ".oe_reset_password_form",
    events: {
        submit: "_onSubmit",
    },

    /**
     * @param {*} ev
     * @returns {void}
     */
    _onSubmit: function (ev) {
        // Tarkista reCAPTCHA-vastaus ennen lomakkeen lähettämistä
        var recaptchaResponse = $("#g-recaptcha-response").val();
        if (!recaptchaResponse) {
            // Jos reCAPTCHA ei ole suoritettu, näytä virheilmoitus
            // Estä lomakkeen oletuslähetys
            ev.preventDefault();
            this.$("#err").text("Please complete the reCAPTCHA verification.");
            return false;
        }

        // Poista virheilmoitus, jos tarkistus onnistuu
        this.$("#err").text("");

        $("#g-recaptcha-response").remove();
    },
});
