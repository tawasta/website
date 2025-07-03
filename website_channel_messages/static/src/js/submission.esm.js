/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { showLoadingOverlay, hideLoadingOverlay } from "@website_utilities/js/loader.esm";
import { showNotification } from "@website_utilities/js/notifications.esm";
import { checkFileSizes } from "@website_skills_qualification/js/files.esm";

export const WebsiteChannelSubmission = publicWidget.Widget.extend({
    selector: "#submission_form.channel_submission",

    start() {
        this._initEditor();
        this._bindEvents();
        return this._super(...arguments);
    },

    async _initEditor() {
        const textarea = this.$("#comment");
        if (!textarea.length) return;

        let lang = "fi";
        if (window.location.pathname.includes("en_US")) lang = "en";
        else if (window.location.pathname.includes("sv_SE")) lang = "sv";

        try {
            this.editor = await ClassicEditor.create(textarea[0], {
                language: lang,
                toolbar: [
                    "heading", "|", "bold", "italic", "link", "bulletedList", "numberedList", "blockQuote", "undo", "redo",
                ],
            });
            this.editor.model.document.on("change:data", () => {
                const text = this.editor.getData().trim();
                this.$("#submission_submit").prop("disabled", !text);
            });
        } catch (error) {
            console.error("CKEditor initialization failed:", error);
        }
    },

    _bindEvents() {
        this.$("#submission_submit").on("click", this._onSubmit.bind(this));
        this.$("#image").on("change", this._onImageChange.bind(this));
        this.$("#file").on("change", this._onFileChange.bind(this));
    },

    async _onSubmit(evt) {
        evt.preventDefault();
        if (!this.editor) {
            showNotification({title: _t("Error!"), message: _t("Editor not initialized."), type: "error", dismissible: true});
            return;
        }
        if (!this.editor.getData().trim()) {
            showNotification({title: _t("Error!"), message: _t("You must add a comment before submitting."), type: "error", dismissible: true});
            return;
        }

        showLoadingOverlay();

        try {
            this.editor.updateSourceElement();
            this.$el[0].submit();
        } finally {
            hideLoadingOverlay();
        }
    },

    _onImageChange(evt) {
        const input = evt.currentTarget;
        const fileTooBig = checkFileSizes(input, this.$("#submission_info_div")[0]);
        if (fileTooBig) {
            $(input).val("");
            this.$("#submission_submit").prop("disabled", true);
            showNotification({title: _t("Error!"), message: _t("File too large. Please select a smaller file."), type: "error", dismissible: true});
            return;
        }
        this._processFile(input.files[0]);
    },

    _onFileChange(evt) {
        const input = evt.currentTarget;
        const fileTooBig = checkFileSizes(input, this.$("#submission_info_div")[0]);
        if (fileTooBig) {
            $(input).val("");
            this.$("#submission_submit").prop("disabled", true);
            showNotification({title: _t("Error!"), message: _t("File too large. Please select a smaller file."), type: "error", dismissible: true});
        }
    },

    _processFile(file) {
        if (!file.type.startsWith("image/")) {
            // Not an image, ignore
            return;
        }
        showLoadingOverlay();

        const reader = new FileReader();
        reader.onload = (event) => {
            const blob = new Blob([event.target.result]);
            const blobURL = window.URL.createObjectURL(blob);
            const image = new Image();
            image.src = blobURL;
            image.onload = () => {
                const resized = this._resizeImage(image);
                const hiddenInput = document.createElement("input");
                hiddenInput.type = "hidden";
                hiddenInput.name = "resized";
                hiddenInput.value = resized;
                this.$el.append(hiddenInput);
                hideLoadingOverlay();
            };
        };
        reader.readAsArrayBuffer(file);
    },

    _resizeImage(img) {
        const MAX_WIDTH = parseInt(this.$("#image").attr("data-maxwidth"), 10);
        const MAX_HEIGHT = parseInt(this.$("#image").attr("data-maxheight"), 10);
        let width = img.width;
        let height = img.height;

        if (width >= height && width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
        } else if (height > width && height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
        }

        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);

        return canvas.toDataURL("image/jpeg");
    },
});

publicWidget.registry.WebsiteChannelSubmission = WebsiteChannelSubmission;
