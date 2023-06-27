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
            }
        };
    });

    return {
        // eslint-disable-next-line no-undef
        toastr: toastr,
    };
});
