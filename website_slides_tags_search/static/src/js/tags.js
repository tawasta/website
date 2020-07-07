odoo.define('website_slides_tags_search.multiple_select', function (require) {
    "use strict";

    var _t = require('web.core')._t;

    $(function () {
        $('#tags-select').select2({
            placeholder: _t("Tags:"),
            allowClear: true,
        });

        $('#tags-select').on('change', function(){
            $('#tags').val($('#tags-select').val().toString());
        });

        console.log("Hello");
    });
});

