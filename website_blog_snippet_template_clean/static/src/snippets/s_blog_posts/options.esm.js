/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

/**
 * Asettaa sarakkeiden asettelun annetulle containerille.
 * @param {HTMLElement} container - Elementti, johon sarakkeet lisätään
 * @param {string} itemSelector - Valitsin elementeille, jotka jaetaan sarakkeisiin
 */
function applyColumnLayout(container, itemSelector = 'div') {
    // Haetaan sarakkeiden määrä attribuutista data-column-count, oletuksena 1
    const count = Number(container.closest('[data-column-count]')?.dataset.columnCount) || 1;

    // Tarkistetaan, onko jo olemassa olevia sarakkeita
    const existingColumns = container.querySelectorAll('.row > .d-flex');
    if (existingColumns.length) {
        // Määritellään Bootstrap-sarakeluokat sarakemäärän mukaan
        const colClassMap = {2: 'col-6', 3: 'col-4', 4: 'col-3', 5: 'col-2', 6: 'col-2'};
        const colClass = colClassMap[count] || 'col-12';

        // Päivitetään olemassa olevien sarakkeiden luokat
        existingColumns.forEach(col => {
            col.className = col.className.replace(/col-\d+/g, '').trim();
            col.classList.add(colClass);
        });

        // Päivitetään containerin luokka sarakemäärän mukaiseksi
        container.className = container.className.replace(/columns-\d+/g, '').trim();
        container.classList.add(`columns-${count}`);
        return;
    }

    // Haetaan kaikki elementit, jotka halutaan jakaa sarakkeisiin
    const items = Array.from(container.querySelectorAll(itemSelector));
    if (!items.length) return;
    // Tyhjennetään container
    container.innerHTML = '';

    const colClassMap = {2: 'col-6', 3: 'col-4', 4: 'col-3', 5: 'col-2', 6: 'col-2'};
    const colClass = colClassMap[count] || 'col-12';

    // Lasketaan kuinka monta itemiä per sarake ja ylijäämät
    const base = Math.floor(items.length / count);
    const extra = items.length % count;
    // Luodaan sarakkeet ja jaetaan itemit niihin
    for (let i = 0; i < count; i++) {
        const colDiv = document.createElement('div');
        colDiv.className = colClass;

        const start = i * base + Math.min(i, extra);
        const end = start + base + (i < extra ? 1 : 0);

        for (let j = start; j < end; j++) {
            colDiv.appendChild(items[j]);
        }

        container.appendChild(colDiv);
    }
    // Päivitetään containerin luokka sarakemäärän mukaiseksi
    container.className = container.className.replace(/columns-\d+/g, '').trim();
    container.classList.add(`columns-${count}`);
}

const DynamicSnippetBlogPostsClean = DynamicSnippet.extend({
    selector: ".s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_template_clean.dynamic_filter_template_blog_post_list_clean']",
    disabledInEditableMode: false,

    async _render() {
        await this._super(...arguments);
        const container = this.el.querySelector('.dynamic_snippet_template');
        if (container) {
            setTimeout(() => {
                console.log("Applying clean layout...");
                applyColumnLayout(container, '.s_blog_posts_post');
            }, 50);  // Viive voi auttaa jos DOM ei ole vielä valmis
        }
    },
});

publicWidget.registry.dynamic_snippet_blog_posts_clean = DynamicSnippetBlogPostsClean;

export { DynamicSnippetBlogPostsClean };
