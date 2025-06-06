/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

/**
 * Sarakkeiden jako tagcloud-snippetille.
 *
 * @param {Element} container - Elementti, johon sarakkeet rakennetaan
 * @param {String} itemSelector - CSS-selector, jolla sisällöt haetaan
 */
function applyColumnLayout(container, itemSelector = "div") {
    const count =
        Number(container.closest("[data-column-count]")?.dataset.columnCount) || 1;

    const items = Array.from(container.querySelectorAll(itemSelector));
    if (!items.length) return;

    container.innerHTML = "";

    const colClassMap = {2: "col-6", 3: "col-4", 4: "col-3", 5: "col-2", 6: "col-2"};
    const colClass = colClassMap[count] || "col-12";

    const base = Math.floor(items.length / count);
    const extra = items.length % count;

    for (let i = 0; i < count; i++) {
        const colDiv = document.createElement("div");
        colDiv.className = colClass;

        const start = i * base + Math.min(i, extra);
        const end = start + base + (i < extra ? 1 : 0);

        for (let j = start; j < end; j++) {
            colDiv.appendChild(items[j]);
        }

        container.appendChild(colDiv);
    }

    container.className = container.className.replace(/columns-\d+/g, "").trim();
    container.classList.add(`columns-${count}`);
}

const DynamicSnippetTagcloud = DynamicSnippet.extend({
    selector: ".s_dynamic_snippet_tagcloud",
    disabledInEditableMode: false,

    _getCategorySearchDomain() {
        const tagcloudCategoryIds = this.$el.get(0).dataset.tagcloudCategoryIds;
        const ids = tagcloudCategoryIds ? JSON.parse(tagcloudCategoryIds) : [];
        return ids.length ? [["category_id", "in", ids.map((tag) => tag.id)]] : [];
    },

    _getSearchDomain() {
        const searchDomain = this._super(...arguments);
        return searchDomain.concat(this._getCategorySearchDomain());
    },

    async _render() {
        await this._super(...arguments);
        const tagContainer = this.el.querySelector(".s_tagcloud_tags");
        if (tagContainer) {
            applyColumnLayout(tagContainer, "a.badge");
        }
    },
});

publicWidget.registry.dynamic_snippet_tagcloud = DynamicSnippetTagcloud;

export {DynamicSnippetTagcloud};
