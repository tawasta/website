odoo.define("website_slides_settings.course.slides.list", function (require) {
    "use strict";

    var websiteSlidesCoursesSlidesList = require("website_slides.course.slides.list");

    websiteSlidesCoursesSlidesList.include({
        /**
         *
         * @override
         */
        _updateHref: function () {
            this.$(".o_wslides_js_slides_list_slide_link").each(function () {
                if (!$(this).hasClass("o_wslides_js_slides_list_slide_link_disable")) {
                    var href = $(this).attr("href");
                    var operator = href.indexOf("?") !== -1 ? "&" : "?";
                    $(this).attr("href", href + operator + "fullscreen=1");
                }
            });
        },
    });
});
