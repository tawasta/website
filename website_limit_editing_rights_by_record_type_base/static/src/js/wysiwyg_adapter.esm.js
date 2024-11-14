/** @odoo-module **/

import {WysiwygAdapterComponent} from "@website/components/wysiwyg_adapter/wysiwyg_adapter";
import {patch} from "@web/core/utils/patch";

patch(WysiwygAdapterComponent.prototype, {
    /**
     * Restrict which terms show up as translatable in the website translation UI
     */
    async startEdition() {
        super.startEdition(...arguments);

        let accessCheckNeeded = false;

        // This function fires also when editing the page, not just translating.
        // Skip all the checks if not translating.
        const inTranslationMode = this.websiteService.context.translation;

        if (inTranslationMode) {
            accessCheckNeeded = await this.userService.hasGroup(
                "website_limit_editing_rights_by_record_type_base.group_website_limit_editing_rights_by_record_type_base"
            );
        }

        if (inTranslationMode && accessCheckNeeded) {
            // Check which models' terms are allowed to be edited
            const recordModel =
                this.env.services.website.currentWebsite.metadata.mainObject.model;

            const recordId =
                this.env.services.website.currentWebsite.metadata.mainObject.id;

            const websiteId = this.env.services.website.currentWebsite.id;

            const allowedModels = await this.env.services.orm.call(
                "website",
                "check_limited_website_editor_access",
                [[websiteId]],
                {record_model: recordModel, record_id: recordId}
            );

            // Filter all elements that are not allowed to be edited, and disable their translation fields.
            // data-oe-model catches 99%, .o_translatable_attribute catches the header search field
            const translationProhibitedElements = $(this.websiteService.pageDocument)
                .find("[data-oe-model], .o_translatable_attribute")
                .filter(function () {
                    const elementModel = $(this).attr("data-oe-model");
                    return !allowedModels.includes(elementModel);
                });

            translationProhibitedElements
                .attr("data-oe-readonly", true)
                .removeAttr("data-oe-translation-state")
                .removeAttr("contenteditable");
        }
    },
});
