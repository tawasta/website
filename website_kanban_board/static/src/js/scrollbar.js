odoo.define('website_kanban_board.kanban_board', function (require) {
    "use strict";

    var core = require('web.core');

    $(function(){
        // Plugin initialization
        $(".fs-whatwg").floatingScroll();

        //Force scrollbar update programmatically
        $(".fs-whatwg").floatingScroll("update");
    });
});
