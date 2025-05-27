/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import dynamicSnippetOptions from "@website/snippets/s_dynamic_snippet/options";

const dynamicSnippetTagcloudOptions = dynamicSnippetOptions.extend({
    init() {
        this._super(...arguments);
        this.modelNameFilter = "blog.tag";
    },

    _setOptionsDefaultValues() {
        // Jos ei ole mitään asetettu, aseta tyhjä listana stringinä
        this._setOptionValue("filterByCategoryIds", JSON.stringify([]));
        this._super(...arguments);
    },
});

options.registry.dynamic_snippet_tagcloud = dynamicSnippetTagcloudOptions;
export default dynamicSnippetTagcloudOptions;
