/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";
import {jsonrpc} from "@web/core/network/rpc_service";

const DynamicSnippetAdvertisement = DynamicSnippet.extend({
    selector: ".s_dynamic_snippet_advertisement",
    disabledInEditableMode: false,

    /**
     * Gets the tag search domain
     *
     * @private
     */
    _getCategorySearchDomain() {
        const searchDomain = [];
        let advertisementCategoryIds = this.$el.get(0).dataset.advertisementCategoryIds;
        advertisementCategoryIds = advertisementCategoryIds
            ? JSON.parse(advertisementCategoryIds)
            : [];
        if (advertisementCategoryIds.length) {
            searchDomain.push([
                "advertisement_category_ids",
                "in",
                advertisementCategoryIds.map((categoryTag) => categoryTag.id),
            ]);
        }
        return searchDomain;
    },

    /**
     * Yhdistetään kaikki domainit
     * @private
     * @override
     */
    _getSearchDomain() {
        const searchDomain = this._super.apply(this, arguments);
        searchDomain.push(...this._getCategorySearchDomain());
        return searchDomain;
    },

    // After rendering, hook into ad elements for tracking
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
            $ad.addEventListener(
                "click",
                () => {
                    jsonrpc(`/advertisement/${adId}/increment_click`, {});
                },
                {once: true}
            );
        });
    },
});

publicWidget.registry.dynamic_snippet_advertisement = DynamicSnippetAdvertisement;
export default DynamicSnippetAdvertisement;
