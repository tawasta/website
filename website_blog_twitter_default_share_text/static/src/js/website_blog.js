odoo.define("website_blog_twitter_default_share_text.website_blog", function (require) {
    "use strict";

    var core = require("web.core");
    var publicWidget = require("web.public.widget");
    var rpc = require("web.rpc");

    publicWidget.registry.websiteBlog.include({
        /**
         * @private
         * @param {Event} ev
         */
        _onShareArticle: function (ev) {
            ev.preventDefault();

            let url = "";

            const $element = $(ev.currentTarget);
            const blogPostTitle = $("#o_wblog_post_name").html() || "";
            const articleURL = window.location.href;
            const windowOpenConfig = "menubar=no, width=500, height=400";

            if ($element.hasClass("o_twitter")) {
                // Query the default share text from website settings in backend
                const websiteId = this._getContext().website_id;

                rpc.query({
                    model: "website",
                    method: "search_read",
                    args: [
                        [["id", "=", websiteId]],
                        ["twitter_default_blog_post_share_text"],
                    ],
                }).then(function (res) {
                    let twitterText = "";
                    if (res[0].twitter_default_blog_post_share_text.trim() === "") {
                        // Fall back to default, if not defined yet
                        twitterText = core._t(
                            "Amazing blog article: %s! Check it live: %s"
                        );
                    } else {
                        twitterText = res[0].twitter_default_blog_post_share_text;
                    }

                    const tweetText = _.string.sprintf(
                        twitterText,
                        blogPostTitle,
                        articleURL
                    );
                    url =
                        "https://twitter.com/intent/tweet?tw_p=tweetbutton&text=" +
                        encodeURIComponent(tweetText);
                    window.open(url, "", windowOpenConfig);
                });
            } else if ($element.hasClass("o_facebook")) {
                url =
                    "https://www.facebook.com/sharer/sharer.php?u=" +
                    encodeURIComponent(articleURL);
                window.open(url, "", windowOpenConfig);
            } else if ($element.hasClass("o_linkedin")) {
                url =
                    "https://www.linkedin.com/sharing/share-offsite/?url=" +
                    encodeURIComponent(articleURL);
                window.open(url, "", windowOpenConfig);
            }
        },
    });
});
