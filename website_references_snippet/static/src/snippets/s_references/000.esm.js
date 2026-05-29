/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

const DynamicSnippetReferences = DynamicSnippet.extend({
    selector: ".s_references_snippet",
    disabledInEditableMode: false,

    /**
     * @override
     */
    start: function () {
        console.debug("[references] start", {
            element: this.el,
            categoryIds: this.el.dataset.filterByCategoryIds,
            filterId: this.el.dataset.filterId,
            templateKey: this.el.dataset.templateKey,
        });

        return this._super.apply(this, arguments);
    },

    /**
     * @override
     * @private
     */
    _getSearchDomain: function () {
        let searchDomain = this._super.apply(this, arguments);
        const rawCategoryIds = this.el.dataset.filterByCategoryIds || "[]";

        let categoryIds = [];
        try {
            categoryIds = JSON.parse(rawCategoryIds)
                .map((id) => parseInt(id))
                .filter((id) => id > 0);
        } catch (error) {
            console.warn("[references] invalid category ids", rawCategoryIds, error);
        }

        if (categoryIds.length) {
            searchDomain = searchDomain.concat([["category_id", "in", categoryIds]]);
        }

        console.debug("[references] search domain", {
            title: this.el.querySelector("h2")?.textContent?.trim(),
            rawCategoryIds: rawCategoryIds,
            categoryIds: categoryIds,
            searchDomain: searchDomain,
        });

        return searchDomain;
    },
});

publicWidget.registry.references = DynamicSnippetReferences;

export default DynamicSnippetReferences;
