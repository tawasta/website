/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import dynamicSnippetOptions from "@website/snippets/s_dynamic_snippet/options";

const DynamicSnippetReferencesOptions = dynamicSnippetOptions.extend({
    /**
     * Same as website_event: restrict dynamic snippet filters to this model.
     *
     * @override
     */
    init() {
        this._super.apply(this, arguments);
        this.modelNameFilter = "res.references";
    },

    /**
     * @override
     */
    _setOptionsDefaultValues() {
        this._setOptionValue("referenceCategoryIds", JSON.stringify([]));
        this._setOptionValue("numberOfRecords", 6);
        this._super.apply(this, arguments);
    },
});

options.registry.references_snippet = DynamicSnippetReferencesOptions;

export default DynamicSnippetReferencesOptions;
