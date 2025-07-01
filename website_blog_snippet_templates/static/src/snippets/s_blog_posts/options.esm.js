/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

function applyColumnLayout(container, itemSelector = "div") {
    const closestEl = container.closest("[data-column-count]");
    const count = Number(closestEl ? closestEl.dataset.columnCount : undefined) || 1;

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

const BlogPostCustomizer = publicWidget.Widget.extend({
    selector:
        ".s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_templates.dynamic_filter_template_blog_post_card_custom'], .s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_templates.dynamic_filter_template_blog_post_list_clean']",

    async start() {
        await this._super(...arguments);

        // Viive varmistaa, että Odoo ehti hakea ja renderöidä postit
        setTimeout(async () => {
            const section = this.el.closest("section");
            const container = section?.querySelector(".dynamic_snippet_template");

            if (container) {
                const elements = await waitForElements(container, ".s_blog_posts_post");

                if (elements) {
                    const showImage =
                        section.getAttribute("data-show_image") === "true";
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
                } else {
                    console.warn("Blog post elements not found within timeout");
                }
            }
        }, 300); // Pieni viive että ehtii varmasti piirtyä
    },
});

publicWidget.registry.blog_post_customizer = BlogPostCustomizer;

export {BlogPostCustomizer};
