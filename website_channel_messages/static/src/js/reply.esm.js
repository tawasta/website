/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ChannelReply = publicWidget.Widget.extend({
    selector: ".submission-section",

    start() {
        this._super(...arguments);
        this._bindEvents();
        this._countThreadMessages();
    },

    _bindEvents() {
        this.$el.on("click", ".btn-reply", this._onReplyClick.bind(this));
        this.$el.on("click", "#reply_badge", this._onReplyBadgeClick.bind(this));
    },

    _onReplyClick(ev) {
        ev.preventDefault();
        console.log("Replying to message...");
        const $btn = $(ev.currentTarget);
        const msgId = $btn.data("msg");
        const msgInfo = $btn.closest(".media-body").children("h5").text();

        $(".message").each((_, el) => {
            const $el = $(el);
            if ($el.data("thread-id") == msgId) {
                $el.addClass("thread-indent");
            } else {
                $el.slideUp(200).removeClass("thread-indent");
            }
        });
        // Poista viimeisestä thread-indent luokka, kuten alkuperäisessä
        $(`.message[data-thread-id='${msgId}']:last`).removeClass("thread-indent");

        $("#reply_msg_badge").text(msgInfo);
        $("#reply_to_msg").val(msgId);
        $("#reply_to_container").removeClass("d-none");
    },

    _onReplyBadgeClick(ev) {
        ev.preventDefault();
        $("#reply_to_msg").val("");
        $("#reply_msg_badge").text("");
        $("#reply_to_container").addClass("d-none");
        $(".message").removeClass("thread-indent").slideDown(100);
    },

    _countThreadMessages() {
        $(".media[data-thread-id]").each((_, el) => {
            const $el = $(el);
            const threadId = $el.data("thread-id");
            const msgCount = $(`.media[data-thread-id='${threadId}']`).length;

            $el.find(".thread-message-counter").text(msgCount);
            if (msgCount > 1) {
                $el.find(".thread-message-container").removeClass("d-none");
            } else {
                $el.find(".thread-message-container").addClass("d-none");
            }
        });
    },
});

export default publicWidget.registry.ChannelReply;
