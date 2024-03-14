/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { _t } from "@web/core/l10n/translation";
import { SlideCoursePage } from '@website_slides/js/slides_course_page';

publicWidget.registry.websiteSlidesCourseSlidesList = SlideCoursePage.extend({

    _updateHref: function () {
        this.$(".o_wslides_js_slides_list_slide_link").each(function () {
            if (!$(this).hasClass("o_wslides_js_slides_list_slide_link_disable")) {
                var href = $(this).attr("href");
                var operator = href.indexOf("?") !== -1 ? "&" : "?";
                $(this).attr("href", href + operator + "fullscreen=1");
            }
        });

        if (this._super) {
            this._super.apply(this, arguments);
        }
    },

});

export default publicWidget.registry.websiteSlidesCourseSlidesList;


/* eslint-disable no-undef, no-negated-condition */
/*
odoo.define("website_slides_settings.course.slides.list", ["@website_slides/js/slides_course_slides_list"], function (require) {
    "use strict";
    var websiteSlidesCourseSlidesList = require("@website_slides/js/slides_course_slides_list");
    console.log("websiteSlidesCourseSlidesList", websiteSlidesCourseSlidesList);
    console.log("prototype", Object.getPrototypeOf(websiteSlidesCourseSlidesList));
    console.log("constructor", websiteSlidesCourseSlidesList.constructor);

    websiteSlidesCourseSlidesList.include({

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
});*/
