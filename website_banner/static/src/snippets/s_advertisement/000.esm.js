/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";
import { jsonrpc } from "@web/core/network/rpc_service";

const DynamicSnippetAdvertisement = DynamicSnippet.extend({
    selector: ".s_dynamic_snippet_advertisement",
    disabledInEditableMode: false,

    _getSearchDomain() {
        const domain = this._super(...arguments);
        const categoryId = parseInt(this.el.dataset.filterByCategoryId || -1);
        if (categoryId >= 0) {
            domain.push(["advertisement_category_id", "=", categoryId]);
        }
        return domain;
    },

    /**
     * @override
     */
    _renderContent() {
        this._super(...arguments);
        this._trackAdvertisementInteractions();
    },

    _trackAdvertisementInteractions() {
        this.el.querySelectorAll("[data-advertisement-id]").forEach(($ad) => {
            const adId = parseInt($ad.dataset.advertisementId);
            if (!adId) return;

            // View count
            jsonrpc(`/advertisement/${adId}/increment_view`, {});

            // Click count
            $ad.addEventListener("click", () => {
                jsonrpc(`/advertisement/${adId}/increment_click`, {});
            }, { once: true });
        });
    },
});

publicWidget.registry.dynamic_snippet_advertisement = DynamicSnippetAdvertisement;
export default DynamicSnippetAdvertisement;
