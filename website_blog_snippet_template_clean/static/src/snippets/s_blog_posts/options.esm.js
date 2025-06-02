/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

/**
 * Asettaa sarakkeiden asettelun annetulle containerille.
 * @param {HTMLElement} container - Elementti, johon sarakkeet lisätään
 * @param {string} itemSelector - Valitsin elementeille, jotka jaetaan sarakkeisiin
 */
function applyColumnLayout(container, itemSelector = 'div') {
    const count = Number(container.closest('[data-column-count]')?.dataset.columnCount) || 1;
    const colClass = {2: 'col-6', 3: 'col-4', 4: 'col-3', 5: 'col-2', 6: 'col-2'}[count] || 'col-12';

    const existingColumns = container.querySelectorAll('.row > .d-flex');
    if (existingColumns.length) {
        existingColumns.forEach(col => {
            col.className = col.className.replace(/col-\d+/g, '').trim();
            col.classList.add(colClass);
        });
        container.className = container.className.replace(/columns-\d+/g, '').trim();
        container.classList.add(`columns-${count}`);
        return;
    }

    const items = Array.from(container.querySelectorAll(itemSelector));
    if (!items.length) return;

    container.innerHTML = '';
    const base = Math.floor(items.length / count);
    const extra = items.length % count;

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

    container.className = container.className.replace(/columns-\d+/g, '').trim();
    container.classList.add(`columns-${count}`);
}

const DynamicSnippetBlogPostsClean = DynamicSnippet.extend({
    selector: ".s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_template_clean.dynamic_filter_template_blog_post_list_clean']",
    disabledInEditableMode: false,

    async _render() {
        await this._super(...arguments);
        const section = this.el.closest('section');
        const container = section?.querySelector('.dynamic_snippet_template');
        if (!container) return;

        // Käytetään requestAnimationFrame DOM-valmiuden varmistamiseksi
        requestAnimationFrame(() => {
            const attrs = {
                showImage: section.dataset.show_image === "true",
                showTags: section.dataset.show_tags === "true",
                showBlog: section.dataset.show_blog === "true",
            };

            if (!attrs.showImage) {
                container.querySelectorAll('.o_record_cover_container').forEach(el => el.remove());
            }
            if (!attrs.showTags) {
                container.querySelectorAll('.small.fw-normal').forEach(el => el.remove());
            }
            if (!attrs.showBlog) {
                container.querySelectorAll('.text-uppercase.text-primary.small.mb-1').forEach(el => el.remove());
            }

            applyColumnLayout(container, '.s_blog_posts_post');
        });
    },
});

publicWidget.registry.dynamic_snippet_blog_posts_clean = DynamicSnippetBlogPostsClean;

export { DynamicSnippetBlogPostsClean };
