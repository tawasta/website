odoo.define('website_utilities.notifications', function (require) {
    "use strict";

    var core = require('web.core');
    var ajax = require("web.ajax");
    var Model = require('web.Model');

    // Upon page reload, check for new messages
    function checkNewMessages() {
        var action = '/new_messages/';
        var msg = "";

        ajax.jsonRpc(action, "call").then(function (res) {
            var response=JSON.parse(res);
            var notification = response['notification_class'];

            if (notification == 'info' && response['msg'] != "") {
                toastr.info(response['msg']);
            } else if (notification == 'success' && response['msg'] != "") {
                toastr.success(response['msg']);
            }
        });
    }

    $(function () {

        var Parameter = new Model("ir.config_parameter");
        Parameter.call('get_param', ['website_utilities.icp_unread_messages_notification']).then(function (enabled) {
            // '1' === enabled
            // '0' === disabled
            if (enabled === '1') {
                checkNewMessages();
            }
        });        

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
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut",
        };
    });

    return {
        toastr: toastr,
    };
});
