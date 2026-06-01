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
            categoryIds: this.el.dataset.referenceCategoryIds,
            filterId: this.el.dataset.filterId,
            templateKey: this.el.dataset.templateKey,
            hasGenericClass: this.el.classList.contains("s_dynamic_snippet"),
        });

        return this._super.apply(this, arguments);
    },

    /**
     * @private
     */
    _getReferenceCategorySearchDomain: function () {
        const rawCategoryIds = this.el.dataset.referenceCategoryIds || "[]";

        let categoryIds = [];
        try {
            categoryIds = JSON.parse(rawCategoryIds)
                .map((category) =>
                    typeof category === "object" && category !== null
                        ? category.id
                        : category
                )
                .map((id) => parseInt(id))
                .filter((id) => id > 0);
        } catch (error) {
            console.warn("[references] invalid category ids", rawCategoryIds, error);
        }

        return categoryIds.length ? [["category_ids", "in", categoryIds]] : [];
    },

    /**
     * @override
     * @private
     */
    _getSearchDomain: function () {
        const searchDomain = this._super.apply(this, arguments);
        return searchDomain.concat(this._getReferenceCategorySearchDomain());
    },
});

publicWidget.registry.references = DynamicSnippetReferences;

export default DynamicSnippetReferences;
