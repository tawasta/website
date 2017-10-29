odoo.define('website_utilities.notifications', function (require) {
    "use strict";

    var core = require('web.core');
    var ajax = require("web.ajax");

    // Upon page reload, check for new messages
    function checkNewMessages() {
        var action = '/new_messages/';
        var msg = "";

        ajax.jsonRpc(action, "call").then(function (res) {
            var response=JSON.parse(res);
            var notifation = response['notification_class'];

            if (notifation == 'info') {
                toastr.info(response['msg']);
            } else {
                toastr.success(response['msg']);
            }
        });
    }

    $(function () {
        checkNewMessages();

        // Toastr -jQuery plugin used for notifications
        toastr.options = {
            "positionClass": "toast-bottom-center",
            "closeButton": true,
            "debug": false,
            "preventDuplicates": true,
            "onclick": null,
            "showDuration": "100",
            "hideDuration": "1000",
            "timeOut": "3000",
            "extendedTimeOut": "1000",
            "tapToDismiss": false,
            "showMethod": "slideDown",
            "hideMethod": "fadeOut",
        };
    });

    return {
        toastr: toastr,
    };
});
