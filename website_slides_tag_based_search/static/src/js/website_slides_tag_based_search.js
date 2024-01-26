odoo.define("website_slides_tag_based_search.tag_search", function () {
    "use strict";

    $(function () {
        const $container = $("#tag_based_slide_search_container");
        const $tagSelect = $("#tag_based_slide_search_input");

        // Keep container hidden until select2 has finished initializing
        $(document).ready(() => {
            // Init tag multiselect
            $tagSelect.select2({
                allowClear: true,
                dropdownAutoWidth: true,
            });

            $container.removeClass("d-none");
        });

        // Set event handler for redirecting to result page
        $("#tag_based_slide_search_submit").on("click", () => {
            const selectedIds = $tagSelect.val();
            let targetUrl = "";

            if (Array.isArray(selectedIds) && selectedIds.length === 0) {
                // If no tag selection made, redirect to channel to show all content
                targetUrl = `${$container.data("target-url")}/`;
            } else {
                // Show loading spinner
                $container.find(".fa-spinner").removeClass("d-none");

                // Form the url and redirect to e.g. /slides/channelname-1/tags/1,2,3/
                const encodedIds = encodeURIComponent(selectedIds.join(","));
                targetUrl = `${$container.data("target-url")}/tags/${encodedIds} `;
            }

            window.location.href = targetUrl;
        });
    });
});
