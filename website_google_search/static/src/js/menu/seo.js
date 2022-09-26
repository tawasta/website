odoo.define("website_google_search.seo", function (require) {
    "use strict";
    // Override the entire HtmlPage class to fix jquery bug in title() function
    var Class = require("web.Class");
    var mixins = require("web.mixins");
    var WORD_SEPARATORS_REGEX =
        "([\\u2000-\\u206F\\u2E00-\\u2E7F'!\"#\\$%&\\(\\)\\*\\+,\\-\\.\\/:;<=>\\?¿¡@\\[\\]\\^_`\\{\\|\\}~\\s]+|^|$)";
    var WebsiteSeo = require("website.seo");
    var HtmlPage = Class.extend(mixins.PropertiesMixin, {
        init: function () {
            mixins.PropertiesMixin.init.call(this);
            this.initTitle = this.title();
            this.defaultTitle = $('meta[name="default_title"]').attr("content");
            this.initDescription = this.description();
        },
        url: function () {
            return window.location.origin + window.location.pathname;
        },
        title: function () {
            return $("head title").text().trim();
        },
        changeTitle: function (title) {
            // TODO create tag if missing
            $("head title").text(title.trim() || this.defaultTitle);
            this.trigger("title-changed", title);
        },
        description: function () {
            return ($("meta[name=description]").attr("content") || "").trim();
        },
        changeDescription: function (description) {
            // TODO create tag if missing
            $("meta[name=description]").attr("content", description);
            this.trigger("description-changed", description);
        },
        keywords: function () {
            var $keywords = $("meta[name=keywords]");
            var parsed =
                $keywords.length > 0 &&
                $keywords.attr("content") &&
                $keywords.attr("content").split(",");
            return parsed && parsed[0] ? parsed : [];
        },
        changeKeywords: function (keywords) {
            // TODO create tag if missing
            $("meta[name=keywords]").attr("content", keywords.join(","));
        },
        headers: function (tag) {
            return $("#wrap " + tag).map(function () {
                return $(this).text();
            });
        },
        getOgMeta: function () {
            var ogImageUrl = $('meta[property="og:image"]').attr("content");
            var title = $('meta[property="og:title"]').attr("content");
            var description = $('meta[property="og:description"]').attr("content");
            return {
                ogImageUrl:
                    ogImageUrl && ogImageUrl.replace(window.location.origin, ""),
                metaTitle: title,
                metaDescription: description,
            };
        },
        images: function () {
            return $("#wrap img")
                .filter(function () {
                    return this.naturalHeight >= 200 && this.naturalWidth >= 200;
                })
                .map(function () {
                    return {
                        src: this.getAttribute("src"),
                        alt: this.getAttribute("alt"),
                    };
                });
        },
        company: function () {
            return $("html").attr("data-oe-company-name");
        },
        bodyText: function () {
            return $("body").children().not(".oe_seo_configuration").text();
        },
        heading1: function () {
            return $("body").children().not(".oe_seo_configuration").find("h1").text();
        },
        heading2: function () {
            return $("body").children().not(".oe_seo_configuration").find("h2").text();
        },
        isInBody: function (text) {
            return new RegExp(
                WORD_SEPARATORS_REGEX + text + WORD_SEPARATORS_REGEX,
                "gi"
            ).test(this.bodyText());
        },
        isInTitle: function (text) {
            return new RegExp(
                WORD_SEPARATORS_REGEX + text + WORD_SEPARATORS_REGEX,
                "gi"
            ).test(this.title());
        },
        isInDescription: function (text) {
            return new RegExp(
                WORD_SEPARATORS_REGEX + text + WORD_SEPARATORS_REGEX,
                "gi"
            ).test(this.description());
        },
        isInHeading1: function (text) {
            return new RegExp(
                WORD_SEPARATORS_REGEX + text + WORD_SEPARATORS_REGEX,
                "gi"
            ).test(this.heading1());
        },
        isInHeading2: function (text) {
            return new RegExp(
                WORD_SEPARATORS_REGEX + text + WORD_SEPARATORS_REGEX,
                "gi"
            ).test(this.heading2());
        },
    });
    WebsiteSeo.SeoConfigurator.include({
        start: function () {
            this._super.apply(this, arguments);
            this.htmlPage = new HtmlPage();
        },
    });
});
