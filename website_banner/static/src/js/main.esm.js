/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.BannerSnippet = publicWidget.Widget.extend({
    selector: ".s_banner_snippet",

    async start() {
        await this._super(...arguments);
        const categoryId = this.el.dataset.categoryId;
        if (!categoryId) {
            console.warn("Banner snippet missing data-category-id");
            return;
        }

        // Funktio, joka päivittää bannerin, kun elementit ovat valmiit
        const updateBanner = async () => {
            const linkEl = this.el.querySelector(".s_banner_link");
            const imgEl = this.el.querySelector(".s_banner_image");

            if (linkEl && imgEl) {
                try {
                    const ad = await jsonrpc(`/ad/render/${categoryId}`, {});
                    if (ad && ad.image && ad.url) {
                        linkEl.href = ad.url;
                        imgEl.src = ad.image;
                        imgEl.alt = ad.title;
                    } else {
                        console.warn("No ad available for this category.");
                    }
                } catch (error) {
                    console.error("Error loading banner ad:", error);
                }
            }
        };

        // MutationObserver seuraa DOM-muutoksia ja käynnistää updateBannerin
        const observer = new MutationObserver((mutations) => {
            for (let mutation of mutations) {
                if (mutation.type === "childList") {
                    updateBanner();
                }
            }
        });

        // Aloitetaan tarkkailu bannerialueen sisällöstä
        observer.observe(this.el, { childList: true, subtree: true });

        // Ensimmäinen päivitys heti alkuun
        updateBanner();
    },
});
