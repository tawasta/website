/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

/**
 * Asettaa sarakkeiden asettelun annetulle containerille.
 * @param {HTMLElement} container - Elementti, johon sarakkeet lisätään
 * @param {string} itemSelector - Valitsin elementeille, jotka jaetaan sarakkeisiin
 */
function applyColumnLayout(container, itemSelector = "div") {
    const count =
        Number(container.closest("[data-column-count]")?.dataset.columnCount) || 1;
    const colClassMap = {2: "col-6", 3: "col-4", 4: "col-3", 5: "col-2", 6: "col-2"};
    const colClass = colClassMap[count] || "col-12";

    // Poistetaan mahdolliset vanhat sarakkeet
    const row = container.querySelector(".row");
    if (!row) return;
    const items = Array.from(row.querySelectorAll(itemSelector));
    if (!items.length) return;

    // Tyhjennetään row
    row.innerHTML = "";

    // Jaetaan itemit uusiin sarakkeisiin
    const base = Math.floor(items.length / count);
    const extra = items.length % count;

    for (let i = 0; i < count; i++) {
        const colDiv = document.createElement("div");
        colDiv.className = `d-flex flex-grow-0 flex-shrink-0 ${colClass}`;
        colDiv.style.flexDirection = "column";

        const start = i * base + Math.min(i, extra);
        const end = start + base + (i < extra ? 1 : 0);

        for (let j = start; j < end; j++) {
            colDiv.appendChild(items[j]);
        }

        row.appendChild(colDiv);
    }

    // Päivitetään containerin luokka sarakemäärän mukaiseksi
    container.className = container.className.replace(/columns-\d+/g, "").trim();
    container.classList.add(`columns-${count}`);
}

const DynamicSnippetBlogPostsClean = DynamicSnippet.extend({
    selector:
        ".s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_templates.dynamic_filter_template_blog_post_card_custom'], .s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_templates.dynamic_filter_template_blog_post_list_clean']",
    disabledInEditableMode: false,

    async _render() {
        await this._super(...arguments);
        const section = this.el.closest("section");
        const container = section?.querySelector(".dynamic_snippet_template");
        if (container) {
            setTimeout(() => {
                const showImage = section.getAttribute("data-show_image") === "true";
                const showTags = section.getAttribute("data-show_tags") === "true";
                const showBlog = section.getAttribute("data-show_blog") === "true";
                if (!showImage) {
                    container
                        .querySelectorAll(".o_record_cover_container")
                        .forEach((el) => el.remove());
                }
                if (!showTags) {
                    container
                        .querySelectorAll(".small.fw-normal")
                        .forEach((el) => el.remove());
                }
                if (!showBlog) {
                    container
                        .querySelectorAll(".text-uppercase.text-primary.small.mb-1")
                        .forEach((el) => el.remove());
                }
                applyColumnLayout(container, ".s_blog_posts_post");
            }, 110); // Viive voi auttaa jos DOM ei ole vielä valmis
        }
    },
});

publicWidget.registry.dynamic_snippet_blog_posts_clean = DynamicSnippetBlogPostsClean;

export {DynamicSnippetBlogPostsClean};
