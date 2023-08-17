odoo.define(
    "website_references_snippet.references",
    function (require) {
        "use strict";

        var core = require("web.core");
        var publicWidget = require("web.public.widget");
        publicWidget.registry.ResReferences = publicWidget.Widget.extend({
            selector: '.references',
            start() {
                let referencesRow = this.el.querySelector('#res-references-row')

                if (referencesRow){
                    this._rpc({
                        route: '/references/',
                        params:{}
                    }).then(data=>{
                        let html = ``
                        data.forEach(reference=>{
                            html += `<div class="pt16 pb16 o_colored_level col-lg-2">
                                    <div class="img img-fluid mx-auto">
                                        <img class="img img-fluid mx-auto" src="data:image/png;base64,${reference.image}"/>
                                    </div>
                            </div>`
                        })
                        referencesRow.innerHTML = html
                    })
                }
            },
        });
    }
);
