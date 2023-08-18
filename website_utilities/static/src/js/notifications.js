odoo.define("website_utilities.notifications", function () {
    "use strict";

    $(function () {
        // Toastr -jQuery plugin used for notifications
        // eslint-disable-next-line no-undef
        $.toastDefaults = {
            position: "bottom-center",
            delay: 5000,
            dismissible: true,
            stackable: true,
            pauseDelayOnHover: true,
            style: {
                toast: "",
                info: "",
                success: "",
                warning: "",
                error: "",
            },
        };

        // You can call the toast with the following syntax:
        // $.toast({
        //     title: "Notice!",
        //     subtitle: "11 mins ago",
        //     content: "Message content",
        //     type: "info",
        //     delay: 50000,
        //     dismissible: true,
        //     img: {
        //         src: "image.png",
        //         class: "rounded",
        //         title: "<a href="https://www.jqueryscript.net/tags.php?/Thumbnail/">Thumbnail</a> Title",
        //         alt: "Alternative"
        //     }
        // });
    });
});
