odoo.define("website_partner_email_prompt.email_prompt", function (require) {
    "use strict";

    var ajax = require("web.ajax");
    var core = require("web.core");
    var Dialog = require("web.Dialog");
    var session = require("web.session");
    require("web.dom_ready");

    // Tarkista käyttäjän sähköpostin olemassaolo
    function checkEmailPrompt() {
        if (session.is_website_user) {
            return;
        }

        var route = "/my/email_check";
        var payload = {
            csrf_token: core.csrf_token,
        };

        ajax.jsonRpc(route, "call", payload).then(function (res) {
            if (res) {
                $("body").append(res);
                $("#emailPromptModal").modal({ backdrop: "static", keyboard: false });
                $("#emailPromptModal").modal("show");
            }
        }).guardedCatch(function () {
            console.error("Error during email check.");
        });
    }

    // Käynnistä tarkistus heti sivun lataamisen jälkeen
    checkEmailPrompt();

    // Lomakkeen lähetys
    $(document).on("submit", "#email_update_form", function (ev) {
        ev.preventDefault();

        var route = "/my/email_update";
        var payload = {
            csrf_token: core.csrf_token,
            email: $("#emailInput").val(),
        };

        ajax.jsonRpc(route, "call", payload).then(function (res) {
            if (res.success) {
                // Näytä onnistumisen dialog
                new Dialog(null, {
                    title: core._t("Success"),
                    size: "medium",
                    $content: $("<div/>").html(res.message),
                    buttons: [
                        {
                            text: core._t("OK"),
                            close: true,
                            click: function () {
                                location.reload(); // Päivitä sivu onnistumisen jälkeen
                            },
                        },
                    ],
                }).open();
            } else {
                // Näytä virhedialog
                new Dialog(null, {
                    title: core._t("Error"),
                    size: "medium",
                    $content: $("<div/>").html(res.error || core._t("An error occurred while updating your email.")),
                    buttons: [
                        {
                            text: core._t("OK"),
                            close: true,
                        },
                    ],
                }).open();
            }
        }).guardedCatch(function () {
            // Odottamaton virhe
            new Dialog(null, {
                title: core._t("Unexpected Error"),
                size: "medium",
                $content: $("<div/>").html(core._t("An unexpected error occurred. Please try again later.")),
                buttons: [
                    {
                        text: core._t("OK"),
                        close: true,
                    },
                ],
            }).open();
        });
    });
});
