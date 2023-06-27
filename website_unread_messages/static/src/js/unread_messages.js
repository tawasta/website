odoo.define("website_unread_messages.unread_messages", function (require) {
    "use strict";

    var ajax = require("web.ajax");
    //var toastr = require("website_utilities.notifications").toastr;

    // Upon page reload, check for new messages
    function checkNewMessages() {
        var action = "/new_messages";

        ajax.jsonRpc(action, "call").then(function (res) {
            var response = JSON.parse(res);
            var isEnabled = response.is_enabled;
            var notification = response.notification_class;
            if (isEnabled && notification === "info" && response.msg !== "") {
                $.toast({
                    title: 'Notice!',
                    subtitle: '11 mins ago',
                    content: response.msg,
                    type: 'info',
                    delay: 50000,
                    dismissible: true,
                    img: {
                        src: 'image.png',
                        class: 'rounded',
                        title: '<a href="https://www.jqueryscript.net/tags.php?/Thumbnail/">Thumbnail</a> Title',
                        alt: 'Alternative'
                    }
                });
                console.log(response.msg);
            } else if (isEnabled && notification === "success" && response.msg !== "") {
                //toastr.success(response.msg);
                console.log(response.msg);
            }
        });
    }

    $(function () {
        checkNewMessages();
    });
});
