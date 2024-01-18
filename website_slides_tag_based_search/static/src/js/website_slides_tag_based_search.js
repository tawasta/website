odoo.define("website_slides_tag_based_search.tag_search", function () {
    "use strict";

    $(function () {
        $("#tag_based_slide_search_submit").on("click", function () {
            const $tagSelect = $("#tag_based_slide_search_input");

            if ($tagSelect.val() === "") {
                return;
            }
            // Read target url from selected option's data attributes, and redirect
            const targetUrl = $tagSelect.find("option:selected").data("target-url");
            window.location.href = targetUrl;
        });
    });
});
