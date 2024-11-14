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
        // proceed with core logic to launch the editor
        super.startEdit(...arguments);
    },
});
