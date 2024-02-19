odoo.define('website_account_request.snippet', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var loadingScreen = require("website_utilities.loader").loadingScreen;

    publicWidget.registry.accountRequestForm = publicWidget.Widget.extend({
        selector: '.s_account_request_form',
        events: {
            'submit': '_onSubmit',
        },

        _onSubmit: function(ev) {
            ev.preventDefault();
            var $form = $(ev.currentTarget);
            var $email = $form.find('#email');
            var $button = $form.find('button[type="submit"]');
            var emailVal = $email.val();
            loadingScreen();
            ajax.jsonRpc('/account/request', 'call', {
                'email': emailVal,
            }).then(function(result) {
                if (result.success) {
                    var loginInfoHtml = "<p>Your account request has been processed successfully.</p>" +
                                        "<p><b>Login:</b> " + result.login + "</p>" +
                                        "<p><b>Password:</b> " + result.password + "</p>" +
                                        "<p>With these credentials, you can log into the demo installation. " +
                                        "<p><a href='/web/login' class='btn btn-primary'>Log In</a></p>";



                    $('#requestSuccessModal .modal-body').html(loginInfoHtml);
                    $('#requestSuccessModal').modal('show');
                    $form[0].reset();
                } else {
                    // Näytä virheviesti
                    console.error("Failed to send account request");
                }
                $.unblockUI();
            });
        },
    });
});
