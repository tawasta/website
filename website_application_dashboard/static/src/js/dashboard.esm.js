/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.dashboard = publicWidget.Widget.extend({
    selector: "#wrapwrap",
    events: {
        "click #app_dashboard_edit": "_editDashboardClick",
        "click #app_dashboard_save": "_saveDashboardClick",
        "click #app_dashboard .app-card:not(.droppable)": "_editAppPosition",
        "click #app_dashboard .app-card.droppable": "_setAppPosition",
        "click #app_dashboard .app-btn-hide": "_toggleVisiblityApp",
        "click #app_dashboard .app-card": "_openApp",
        "click #app_dashboard .app-info": "_openInfo",
        "click #app_dashboard .app-btn-delete": "_deleteApp",
    },

    /**
     * @class
     */
    init: function () {
        // Check if editing
        const url = new URL(window.location);
        $("#position_before").select2();
        if (url.searchParams.has("editing")) {
            $("#app_dashboard_edit").addClass("d-none");
            $("#app_dashboard_save").removeClass("d-none");
            $("#editing_info").removeClass("d-none");
            $(".app-btn-hide").removeClass("d-none");
            $("#app_dashboard").addClass("editing-dashboard");
            $(".app-card-create").removeClass("d-none");
            $(".app-btn-delete").removeClass("d-none");
        }
        this._super.apply(this, arguments);
        this.rpc = this.bindService("rpc");
    },

    // --------------------------------------------------------------------------
    // Handlers
    // --------------------------------------------------------------------------

    /**
     * Open page in edit mode
     *
     * @private
     * @param {Event} ev
     */
    _editDashboardClick: function (ev) {
        ev.preventDefault();
        $(ev.currentTarget).addClass("d-none");
        $("#app_dashboard_save").removeClass("d-none");
        $("#editing_info").removeClass("d-none");
        $(".app-btn-hide").removeClass("d-none");
        $("#app_dashboard").addClass("editing-dashboard");
        $(".app-card-create").removeClass("d-none");
        $(".app-btn-delete").removeClass("d-none");
        $(".create-card").removeClass("d-none");
        const url = new URL(window.location);
        url.searchParams.set("editing", 1);
        window.history.replaceState(null, null, url.toString());
    },

    /**
     * Commit changes and reload page
     *
     * @private
     * @param {Event} ev
     */
    _saveDashboardClick: function (ev) {
        ev.preventDefault();
        $("#app_dashboard_save").addClass("d-none");
        $("#app_dashboard_edit").removeClass("d-none");
        $("#editing_info").addClass("d-none");
        $(".app-btn-hide").addClass("d-none");
        $(".create-card").addClass("d-none");
        $("#app_dashboard").removeClass("editing-dashboard");
        $(".app-btn-delete").addClass("d-none");
        const url = new URL(window.location);
        url.searchParams.delete("editing");
        window.history.replaceState(null, null, url.toString());
        // Calculate card positions, submit and save in controller
        const data = {};
        const self = this;
        $(".card:not(.create-card)")
            .each(function (el) {
                const card = $(this).closest(".app-card");
                data[$(this).attr("app-id")] = {
                    position: el,
                    hidden: $(card).hasClass("app-hidden"),
                    removed: $(card).hasClass("removed"),
                };
            })
            .promise()
            .done(function () {
                return self.rpc("/dashboard/save", {
                    data: data,
                });
            });
    },

    /**
     * Edit app position
     *
     * @private
     * @param {Event} ev
     */
    _editAppPosition: function (ev) {
        ev.preventDefault();
        // Check we are in editing mode
        const url = new URL(window.location);
        const card = $(ev.target).closest(".app-card");
        if (url.searchParams.has("editing") && !$(card).hasClass("not-droppable")) {
            $(card).addClass("editing-app");
            // Droppable only in same category
            const categId = $(card).data("category");
            const selector = `.app-card[data-category='${categId}']:not(.editing-app)`;
            $(".app-card:not(.editing-app)").addClass("not-droppable");
            $(selector).removeClass("not-droppable").addClass("droppable");
        }
    },

    /**
     * We prepend the app before selected element
     * and save sequence
     *
     * @private
     * @param {Event} ev
     */
    _setAppPosition: function (ev) {
        ev.preventDefault();
        const target = $(ev.target).closest(".app-card");
        $(".editing-app").insertBefore(target);
        // Clean up
        $(".app-card")
            .removeClass("editing-app")
            .removeClass("droppable")
            .removeClass("not-droppable");
    },

    /**
     * Hide/show application from user
     *
     * @private
     * @param {Event} ev
     */
    _toggleVisiblityApp: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const target = $(ev.target).closest(".app-card");
        $(target).toggleClass("app-hidden");
        const hideText = $(target).find(".app-hide-text");
        const showText = $(target).find(".app-show-text");
        $(target).find(".app-btn-hide > span").addClass("d-none");
        if ($(target).hasClass("app-hidden")) {
            $(showText).removeClass("d-none");
        } else {
            $(hideText).removeClass("d-none");
        }
    },

    /**
     * Open application
     *
     * @private
     * @param {Event} ev
     */
    _openApp: function (ev) {
        // Check that we are not editing
        if (!$("#app_dashboard").hasClass("editing-dashboard")) {
            ev.preventDefault();
            ev.stopPropagation();
            const card = $(ev.target).closest(".card");
            window.open($(card).data("href"), "_blank").focus();
        }
    },

    /**
     * Open info
     *
     * @private
     * @param {Event} ev
     */
    _openInfo: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const info = $(ev.target).data("info") || "";
        $("#application_info_text").html(info);
        $("#modal_application_info").modal("show");
    },

    /**
     * Delete own app
     *
     * @private
     * @param {Event} ev
     */
    _deleteApp: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        // Add effect when clicking remove, delete when clicking "Save"
        const target = $(ev.target).closest(".app-card");
        $(target).addClass("removed");
        $(target).fadeOut();

        // eslint-disable-next-line no-undef
        const toast = new Toast(document.getElementById("removed_app_toast"));
        toast.show();
    },
});
