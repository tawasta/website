/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { showNotification } from "@website_utilities/js/notifications.esm"; // varmista polku

function checkNewMessages() {
    const action = "/new_messages";

    jsonrpc(action, {}).then((responseRaw) => {
        const response = typeof responseRaw === "string" ? JSON.parse(responseRaw) : responseRaw;
        const isEnabled = response.is_enabled;
        const notification = response.notification_class;
        const message = response.msg;

        if (isEnabled && message) {
            showNotification({
                title:
                    notification === "success"
                        ? _t("Success!")
                        : notification === "error"
                        ? _t("Error!")
                        : _t("Notice!"),
                message,
                type: notification,
                dismissible: true,
            });
        }
    });
}

$(document).ready(() => {
    checkNewMessages();
});
