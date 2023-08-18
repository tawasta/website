odoo.define("website_channel_messages.thread", function (require) {
    "use strict";

    var core = require("web.core");
    var ajax = require("web.ajax");
    var _t = core._t;

    require("web.dom_ready");

    function updateMessages() {
        var record = parseInt($("#maincontent").attr("data-record-id"), 10) || 0;
        var route = "/website_channel/update_messages";
        var timestamp = $("#maincontent").attr("data-timestamp");
        var payload = {
            channel_id: record,
            timestamp: timestamp,
            csrf_token: core.csrf_token,
        };
        var msg = "";
        if (document.hasFocus()) {
            ajax.jsonRpc(route, "call", payload).then(function (res) {
                if (res !== "") {
                    var new_date = new Date().getTime() / 1000;
                    $("#maincontent").attr("data-timestamp", new_date);
                    var cleaned = res.replace("data-src", "src");
                    $("#channel_messages").prepend(cleaned);
                    msg = _t("New message arrived!");
                    console.log(msg);
                    $.toast({
                        title: _t("Notice!"),
                        subtitle: _t("Messages"),
                        content: msg,
                        type: "info",
                        delay: 5000,
                        dismissible: true,
                    });
                }
            });
        }
    }

    var record = $("#maincontent").attr("data-record-id");

    if (record !== undefined) {
        $(window).scroll(function () {
            $(".msg-img").each(function () {
                var bot_obj = $(this).offset().top + $(this).outerHeight();
                var bot_window = $(window).scrollTop() + $(window).height();
                if (bot_window > bot_obj && $(this).attr("src") === undefined) {
                    $(this).attr("src", $(this).attr("data-src"));
                }
            });
        });
        setTimeout(function () {
            $(window).scroll();
        }, 100);

        setInterval(function () {
            updateMessages();
        }, $("#channel_messages").attr("data-interval"));
    }
});
