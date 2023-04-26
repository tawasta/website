odoo.define("website_channel_messages.reply", function (require) {
    "use strict";

    require("web.dom_ready");

    $(document).on("click", ".btn-reply", function () {
        // Get reply msg ID from data, add it to submission form
        var msgId = $(this).data("msg");
        var msgInfo = $(this).closest(".media-body").children("h5").text();

        // Hide other messages than the thread
        $(".message[data-thread-id='" + msgId + "']").addClass("thread-indent");
        $(".message[data-thread-id='" + msgId + "']:last").removeClass("thread-indent");
        $(".message:not([data-thread-id='" + msgId + "'])").slideUp(200);

        // Add badge to show which it is a reply to (and possibility to remove it)
        $("#reply_msg_badge").text(msgInfo);
        $("#reply_to_msg").val(msgId);
        $("#reply_to_container").removeClass("d-none");
    });

    $(document).on("click", "#reply_badge", function () {
        $("#reply_to_msg").val("");
        $("#reply_msg_badge").text("");
        $("#reply_to_container").addClass("d-none");
        $(".message").removeClass("thread-indent").slideDown(100);
    });

    $(document).on("click", ".reply-ref-container .card", function () {
        var msgId = $(this).data("target");
        $(".pulse").removeClass("pulse");
        $("#" + msgId).addClass("pulse");
        $([document.documentElement, document.body]).animate(
            {
                scrollTop: $("#" + msgId).offset().top - 70,
            },
            1000
        );
    });
});
