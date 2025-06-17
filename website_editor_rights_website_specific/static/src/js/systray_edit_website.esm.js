/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";

// Access the "Edit" systray button via the registry
const EditWebsiteSystray = registry
    .category("website_systray")
    .get("EditWebsite").Component;

patch(EditWebsiteSystray.prototype, {
    /**
     * Patch the startEdit function to be async, and
     * do the access rights check to backend before launching the
     * editor.
     */
    async startEdit() {
        const websiteId = this.env.services.website.currentWebsite.id;

        await this.env.services.orm.call(
            "website",
            "check_website_specific_editor_access",
            [[websiteId]],
            {}
        );

        // If no accessDenied error raised in backend,
        // proceed with core logic to launch the editor
        super.startEdit(...arguments);
    },
});
