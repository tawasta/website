odoo.define('web_environment_ribbon.ribbon', function (require) {
    "use strict";

    var $ = require('jquery');
    var rpc = require('web.rpc');
    var core = require('web.core');

    $( document ).ready(function () {

        var ribbon = $('<div class="test-ribbon hidden"/>');
        $('body').append(ribbon);
        ribbon.hide();
        // Get ribbon data from backend
        rpc.query({
            model: 'web.environment.ribbon.backend',
            method: 'get_environment_ribbon',
        }).then(
            function (ribbon_data) {
            // Ribbon name
                if (ribbon_data.name && ribbon_data.name !== 'False') {
                    ribbon.html(ribbon_data.name);
                    ribbon.show();
                }
                // Ribbon color
                if (ribbon_data.color && validStrColour(ribbon_data.color)) {
                    ribbon.css('color', ribbon_data.color);
                }
                // Ribbon background color
                if (ribbon_data.background_color && validStrColour(ribbon_data.background_color)) {
                    ribbon.css('background-color', ribbon_data.background_color);
                }
            },
        );
    });
});
