/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";

// Access the "Translate" systray button via the registry
const TranslateWebsiteSystray = registry
    .category("website_systray")
    .get("TranslateWebsiteSystray").Component;

patch(TranslateWebsiteSystray.prototype, {
    /**
     * Patch the startTranslate function to be async, and
     * do the access rights check to backend before launching the
     * translation view.
     */

    async startTranslate() {
        console.log("START TRANSLATE REACHED");
        const websiteId = this.env.services.website.currentWebsite.id;

        await this.env.services.orm.call(
            "website",
            "check_website_specific_editor_access",
            [[websiteId]],
            {}
        );

        // If no accessDenied error raised in backend,
        // proceed with core logic to launch the translation editor
        super.startTranslate(...arguments);
    },
});
