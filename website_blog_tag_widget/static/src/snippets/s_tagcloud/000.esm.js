/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";
import {jsonrpc} from "@web/core/network/rpc_service";

const DynamicSnippetTagcloud = DynamicSnippet.extend({
    selector: ".s_dynamic_snippet_tagcloud",
    disabledInEditableMode: false,

    /**
     * Gets the tag search domain
     *
     * @private
     */
    _getCategorySearchDomain() {
        const searchDomain = [];
        let tagcloudCategoryIds = this.$el.get(0).dataset.tagcloudCategoryIds;
        tagcloudCategoryIds = tagcloudCategoryIds
            ? JSON.parse(tagcloudCategoryIds)
            : [];
        if (tagcloudCategoryIds.length) {
            searchDomain.push([
                "category_id",
                "in",
                tagcloudCategoryIds.map((categoryTag) => categoryTag.id),
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
});

publicWidget.registry.dynamic_snippet_tagcloud = DynamicSnippetTagcloud;
export default DynamicSnippetTagcloud;
