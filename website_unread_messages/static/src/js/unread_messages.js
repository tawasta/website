odoo.define('website_unread_messages.unread_messages', function (require) {
    "use strict";

    var core = require('web.core');
    var ajax = require("web.ajax");
    var Model = require('web.Model');
    var toastr = require('website_utilities.notifications').toastr;

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
        var externalId = 'website_unread_messages.icp_unread_messages_notification';
        Parameter.call('get_param', [externalId]).then(function (enabled) {
            // '1' === enabled
            // '0' === disabled
            if (enabled === '1') {
                checkNewMessages();
            }
        });        
    });
});
