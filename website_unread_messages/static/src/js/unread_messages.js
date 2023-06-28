odoo.define("website_unread_messages.unread_messages", function (require) {
    "use strict";

    var ajax = require("web.ajax");
    var _t = require("web.core")._t;

    // Upon page reload, check for new messages
    function checkNewMessages() {
        var action = "/new_messages";

        ajax.jsonRpc(action, "call").then(function (res) {
            var response = JSON.parse(res);
            var isEnabled = response.is_enabled;
            var notification = response.notification_class;
            if (isEnabled && notification === "info" && response.msg !== "") {
                $.toast({
                    title: _t("Notice!"),
                    subtitle: _t("New messages"),
                    content: response.msg,
                    type: "info",
                    delay: 5000,
                    dismissible: true
                });
            } else if (isEnabled && notification === "success" && response.msg !== "") {
                console.log(response.msg);
                $.toast({
                    title: _t("Success!"),
                    subtitle: _t("New messages"),
                    content: response.msg,
                    type: "success",
                    delay: 5000,
                    dismissible: true
                });
            }
        });
    }

    $(function () {
        checkNewMessages();
    });
});
