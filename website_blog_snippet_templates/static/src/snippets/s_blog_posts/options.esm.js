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

    // Tyhjennä ja rakenna sarakkeet uusiksi
    row.innerHTML = "";

    // Luo sarakkeet
    const cols = [];
    for (let i = 0; i < count; i++) {
        const colDiv = document.createElement("div");
        colDiv.className = `d-flex flex-grow-0 flex-shrink-0 ${colClass}`;
        colDiv.style.flexDirection = "column";
        cols.push(colDiv);
        row.appendChild(colDiv);
    }

    // Jaa postit "tavallisesti" riveittäin:
    // 1 -> col0, 2 -> col1, 3 -> col2, 4 -> col0, ...
    items.forEach((item, idx) => {
        cols[idx % count].appendChild(item);
    });

    // Päivitä containerin helper-luokka
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
                return;
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
        ".s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_templates.dynamic_filter_template_blog_post_card_custom'], " +
        ".s_dynamic_snippet_blog_posts[data-template-key='website_blog_snippet_templates.dynamic_filter_template_blog_post_list_clean']",

    async start() {
        await this._super(...arguments);

        // Viive varmistaa, että Odoo ehti hakea ja renderöidä postit
        setTimeout(async () => {
            const section = this.el.closest("section");
            const container = section?.querySelector(".dynamic_snippet_template");

            if (!container) return;

            const elements = await waitForElements(container, ".s_blog_posts_post");
            if (!elements) {
                console.warn("Blog post elements not found within timeout");
                return;
            }

            const showImage = section.getAttribute("data-show_image") === "true";
            const showTags = section.getAttribute("data-show_tags") === "true";
            const showBlog = section.getAttribute("data-show_blog") === "true";

            // Poista kuva, jos valittu pois
            if (!showImage) {
                container
                    .querySelectorAll(".o_record_cover_container")
                    .forEach((el) => el.remove());
            }

            // Poista tagit, jos valittu pois
            // Huom: tämä osuu sekä clean-list että card-layoutiin (badge/tag-alueet)
            if (!showTags) {
                container
                    .querySelectorAll(".fw-normal, .d-flex.flex-wrap.gap-2")
                    .forEach((el) => el.remove());
            }

            // Poista blogin nimi (clean-listissä se on tuo text-uppercase...)
            if (!showBlog) {
                container
                    .querySelectorAll(".text-uppercase.text-primary.small.mb-1")
                    .forEach((el) => el.remove());
            }

            // Sarake-layout (riveittäin vasemmalta oikealle)
            applyColumnLayout(container, ".s_blog_posts_post");
        }, 600);
    },
});

publicWidget.registry.blog_post_customizer = BlogPostCustomizer;

export {BlogPostCustomizer};
