/** @odoo-module **/

import {jsonRpc} from "@web/core/network/rpc_service";

export function trackAdvertisementInteractions(root) {
    root.querySelectorAll("[data-advertisement-id]").forEach(($ad) => {
        const adId = parseInt($ad.dataset.advertisementId);
        if (!adId) return;

        // View count
        jsonRpc("/advertisement/increment_view", {
            args: [adId],
        });

        // Click count
        $ad.addEventListener(
            "click",
            () => {
                jsonRpc("/advertisement/increment_click", {
                    args: [adId],
                });
            },
            {once: true}
        ); // Lasketaan vain 1 klikkaus
    });
}
