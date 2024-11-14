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
        // Check what kind of record's page is being edited
        const recordModel =
            this.env.services.website.currentWebsite.metadata.mainObject.model;

        const recordId =
            this.env.services.website.currentWebsite.metadata.mainObject.id;

        const websiteId = this.env.services.website.currentWebsite.id;

        await this.env.services.orm.call(
            "website",
            "check_limited_website_editor_access",
            [[websiteId]],
            {record_model: recordModel, record_id: recordId}
        );

        // If no accessDenied error raised in backend,
        // proceed with core logic to launch the translation editor
        super.startTranslate(...arguments);
    },
});
