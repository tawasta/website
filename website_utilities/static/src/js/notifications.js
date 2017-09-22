odoo.define('website_utilities.notifications', function (require) {
    "use strict";

    var core = require('web.core');
    var ajax = require("web.ajax");
    var _t = core._t;

    // Upon page reload, check for new messages
    function checkNewMessages() {
        var action = '/new_messages/';
        var msg = "";

        ajax.jsonRpc(action, "call").then(function (res) {
            // var link_part_start = "<a href='/medical/discussion/'>";
            // var link_part_end = "</a>";
            var msg_parts = "";
            if (res == 1) {
                msg_parts += _t("You have ");
                msg_parts += _t("a new message!");
                // msg += link_part_start;
                msg += msg_parts;
                // msg += link_part_end;
                toastr.info(msg);
            } else if (res > 1) {
                msg_parts += _t("You have ");
                msg_parts += res.toString();
                msg_parts += _t(" new messages!");
                // msg += link_part_start;
                msg += msg_parts;
                // msg += link_part_end;
                toastr.info(msg);
            } else {
                if (res == -1) {
                    return false;
                } else {
                    msg = _t("There aren't any new messages!");
                    toastr.success(msg);
                }
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
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": 0,
            "extendedTimeOut": 0,
            "tapToDismiss": false
        };
    });

    return {
        toastr: toastr,
    };
});
