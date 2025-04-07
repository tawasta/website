/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.PartnerDataPrompt = publicWidget.Widget.extend({
    selector: '#wrap',

    start: function () {
        this._super.apply(this, arguments);
        this._showPromptIfNeeded();
    },

    _showPromptIfNeeded: function () {
        jsonrpc("/my/data_check", {}).then(modalHtml => {
            if (!modalHtml) return;
            const $modal = $(modalHtml);
            $modal.find(".modal-body > div").removeClass("container");
            $modal.appendTo(document.body);
            const modalInstance = new Modal($modal[0], {backdrop: 'static', keyboard: false});
            modalInstance.show();

            $modal.on("shown.bs.modal", function () {
                $modal.find("select.select2").select2({
                    width: '100%',
                    placeholder: "Select an option",
                    dropdownParent: $modal
                });
            });

            $modal.on("hidden.bs.modal", function () {
                $modal.remove();
            });
        }).catch(err => {
            console.error("Modal loading failed", err);
        });
    },
});
