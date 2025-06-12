/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import DynamicSnippet from "@website/snippets/s_dynamic_snippet/000";

function applyColumnLayout(container, itemSelector = "div") {
    const count =
        Number(container.closest("[data-column-count]")?.dataset.columnCount) || 1;
    const colClassMap = {2: "col-6", 3: "col-4", 4: "col-3", 5: "col-2", 6: "col-2"};
    const colClass = colClassMap[count] || "col-12";

    const row = container.querySelector(".row");
    if (!row) return;
    const items = Array.from(row.querySelectorAll(itemSelector));
    if (!items.length) return;

    row.innerHTML = "";

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

    container.className = container.className.replace(/columns-\d+/g, "").trim();
    container.classList.add(`columns-${count}`);
    console.log("=========MENEEHAN TANNE===========");
}

function waitForElements(container, selector, timeout = 3000) {
    return new Promise((resolve) => {
        const intervalTime = 100;
        let timeSpent = 0;

        const interval = setInterval(() => {
            const elements = container.querySelectorAll(selector);
            if (elements.length) {
                clearInterval(interval);
                resolve(elements);
            }
            timeSpent += intervalTime;
            if (timeSpent >= timeout) {
                clearInterval(interval);
                resolve(null);
            }
        }, intervalTime);
    });
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
            const showImage = section.getAttribute("data-show_image") === "true";
            const showTags = section.getAttribute("data-show_tags") === "true";
            const showBlog = section.getAttribute("data-show_blog") === "true";

            if (!showImage) {
                container.querySelectorAll(".o_record_cover_container").forEach(el => el.remove());
            }
            if (!showTags) {
                container.querySelectorAll(".small.fw-normal").forEach(el => el.remove());
            }
            if (!showBlog) {
                container.querySelectorAll(".text-uppercase.text-primary.small.mb-1").forEach(el => el.remove());
            }

            const elements = await waitForElements(container, ".s_blog_posts_post");
            if (elements) {
                applyColumnLayout(container, ".s_blog_posts_post");
            } else {
                console.warn("Blog post elements not found within timeout");
            }
        }
    },
});

publicWidget.registry.dynamic_snippet_blog_posts_clean = DynamicSnippetBlogPostsClean;

export { DynamicSnippetBlogPostsClean };
