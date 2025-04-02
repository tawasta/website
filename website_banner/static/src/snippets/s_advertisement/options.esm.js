/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import dynamicSnippetOptions from "@website/snippets/s_dynamic_snippet/options";

const dynamicSnippetAdvertisementOptions = dynamicSnippetOptions.extend({
    init() {
        this._super(...arguments);
        this.modelNameFilter = "advertisement.advertisement";
        this.categories = {};
    },

    async _renderCustomXML(uiFragment) {
        await this._super(...arguments);
        await this._renderCategorySelector(uiFragment);
    },

    async _renderCategorySelector(uiFragment) {
        const result = await this.orm.searchRead("advertisement.category", [], ["id", "name"]);
        this.categories = Object.fromEntries(result.map((c) => [c.id, c]));
        const el = uiFragment.querySelector('[data-name="category_opt"]');
        return this._renderSelectUserValueWidgetButtons(el, this.categories);
    },

    _setOptionsDefaultValues() {
        this._setOptionValue("filterByCategoryId", -1);
        this._super(...arguments);
    },
});

options.registry.dynamic_snippet_advertisement = dynamicSnippetAdvertisementOptions;
export default dynamicSnippetAdvertisementOptions;
