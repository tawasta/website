odoo.define("website_application_dashboard.dashboard", function (require) {
    "use strict";

    const publicWidget = require("web.public.widget");
    publicWidget.registry.dashboard = publicWidget.Widget.extend({
        selector: "#app_dashboard",
        events: {
            "click #app_dashboard_edit": "_editDashboardClick",
            "click #app_dashboard_save": "_saveDashboardClick",
            "click .app-card:not(.droppable)": "_editAppPosition",
            "click .app-card.droppable": "_setAppPosition",
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
            // Calculate card positions, submit and save in controller
            const positions = {};
            const self = this;
            $(".card")
                .each(function (el) {
                    positions[$(this).attr("app-id")] = el;
                })
                .promise()
                .done(function () {
                    return self._rpc({
                        route: "/dashboard/save",
                        params: {
                            positions: positions,
                            // TODO: Visibility
                        },
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
            if (url.searchParams.has("editing")) {
                $(ev.target).closest(".app-card").addClass("editing-app");
                $(".app-card:not(.editing-app)").addClass("droppable");
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
            $(".app-card").removeClass("editing-app").removeClass("droppable");
        },
    });
});
