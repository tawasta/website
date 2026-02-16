/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { showNotification } from "@website_utilities/js/notifications.esm";
import publicWidget from "@web/legacy/js/public/public_widget";

export const WebsiteChannelMessagesThread = publicWidget.Widget.extend({
    selector: "#maincontent_channel",

    start() {
        this._super(...arguments);
        this._bindScrollLazyLoad();
        this._startUpdateInterval();
    },

    _bindScrollLazyLoad() {
        $(window).on("scroll", () => {
            $(".msg-img").each(function () {
                const botObj = $(this).offset().top + $(this).outerHeight();
                const botWindow = $(window).scrollTop() + $(window).height();
                if (botWindow > botObj && !$(this).attr("src")) {
                    $(this).attr("src", $(this).attr("data-src"));
                }
            });
        });

        // Trigger once immediately after load
        setTimeout(() => {
            $(window).trigger("scroll");
        }, 100);
    },

    _startUpdateInterval() {
        const interval = parseInt($("#channel_messages").attr("data-interval"), 10) || 30000;
        setInterval(() => this._updateMessages(), interval);
    },

    async _updateMessages() {
        if (!document.hasFocus()) {
            return;
        }

        const record = parseInt(this.$el.data("record-id"), 10) || 0;
        if (!record) {
            return;
        }

        const timestamp = this.$el.data("timestamp");
        const payload = {
            channel_id: record,
            timestamp,
            csrf_token: odoo.csrf_token,
        };

        try {
            const res = await jsonrpc("/website_channel/update_messages", payload);
            if (res && res !== "") {
                const newTimestamp = Date.now() / 1000;
                this.$el.data("timestamp", newTimestamp);
                const cleaned = res.replace(/data-src/g, "src");
                $("#channel_messages").prepend(cleaned);

                showNotification({
                    title: _t("Notice!"),
                    message: _t("New message arrived!"),
                    type: "info",
                    dismissible: true,
                });
                console.log(_t("New message arrived!"));
            }
        } catch (error) {
            console.error("Failed to update messages:", error);
        }
    },
});

publicWidget.registry.WebsiteChannelMessagesThread = WebsiteChannelMessagesThread;
