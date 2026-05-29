/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

const DynamicSnippetReferences = DynamicSnippet.extend({
    selector: ".s_references_snippet",
    disabledInEditableMode: false,

    /**
     * Same pattern as website_event:
     * read selected ids from dataset and extend search domain.
     *
     * @override
     * @private
     */
    _getSearchDomain: function () {
        let searchDomain = this._super.apply(this, arguments);
        const filterByCategoryIds = this.$el.get(0).dataset.filterByCategoryIds;

        if (filterByCategoryIds) {
            const categoryIds = JSON.parse(filterByCategoryIds);
            if (categoryIds.length) {
                searchDomain = searchDomain.concat([
                    ["category_id", "in", categoryIds],
                ]);
            }
        }

        return searchDomain;
    },
});

publicWidget.registry.references = DynamicSnippetReferences;

export default DynamicSnippetReferences;