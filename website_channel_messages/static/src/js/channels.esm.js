/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { showNotification } from "@website_utilities/js/notifications.esm";

publicWidget.registry.WebsiteChannelMessages = publicWidget.Widget.extend({
    selector: "#modal_create_channel",

    start() {
        this._super(...arguments);
        this._initSelect2();
        this._bindEvents();
    },

    _initSelect2() {
        if (window.$ && $.fn.select2) {
            $(".select2").select2();
        }
    },

    _bindEvents() {
        this.$el.on("click", "#create_channel_confirm", this._onCreateChannelConfirm.bind(this));
    },

    async _onCreateChannelConfirm() {
        const partner_ids = $("#recipients").select2("val").map(Number);

        if (partner_ids.length === 0) {
            showNotification({
                title: _t("Error!"),
                message: _t("You must select recipient!"),
                type: "error",
                dismissible: true,
            });
            return;
        }

        try {
            const payload = {
                recipients: partner_ids,
                csrf_token: odoo.csrf_token,
            };

            const res = await jsonrpc("/website_channel/create", payload);
            const channel_id = res.id;

            if (!document.querySelector(`#channel_${channel_id}`)) {
                location.reload();
            } else {
                const msg =
                    _t("You already have a chat with these recipients.") +
                    `<br/><a href='/website_channel/${channel_id}'><b>${_t("Click here to open channel")}</b></a>.`;

                showNotification({
                    title: _t("Notice!"),
                    message: msg,
                    type: "info",
                    dismissible: true,
                });

                this.$el.modal("hide");
            }
        } catch (error) {
            showNotification({
                title: _t("Error!"),
                message: error.message || _t("Failed to create channel."),
                type: "error",
                dismissible: true,
            });
        }
    },
});

export default publicWidget.registry.WebsiteChannelMessages;
