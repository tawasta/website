odoo.define("website_channel_messages.reply", function (require) {
    "use strict";

    require("web.dom_ready");

    $(document).on("click", ".btn-reply", function () {
        // Get reply msg ID from data, add it to submission form
        console.log("Replying to message...");
        var msgId = $(this).data("msg");
        var msgInfo = $(this).closest(".media-body").children("h5").text();

        // Hide other messages than the thread
        $(".message[data-thread-id='" + msgId + "']").addClass("thread-indent");
        $(".message[data-thread-id='" + msgId + "']:last").removeClass("thread-indent");
        $(".message:not([data-thread-id='" + msgId + "'])").slideUp(200);
        console.log("Hid other messages...");

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

    // Count thread messages for every thread
    $(".media[data-thread-id]").each(function (key, el) {
        const threadId = $(el).data("thread-id");
        const msgCount = $(".media[data-thread-id=" + threadId + "]").length;
        $(el).find(".thread-message-counter").text(msgCount);

        if (msgCount > 1) {
            $(el).find(".thread-message-container").removeClass("d-none");
        } else {
            $(el).find(".thread-message-container").addClass("d-none");
        }
    });
});