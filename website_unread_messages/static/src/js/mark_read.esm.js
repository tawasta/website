/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";

$(document).ready(() => {
    $(".read-confirm").on("click", async () => {
        await jsonrpc("/web/dataset/call_kw/mail.message/mark_all_as_read", {
            model: "mail.message",
            method: "mark_all_as_read",
            args: [],
            kwargs: {},
        });
        location.reload();
    });
});
