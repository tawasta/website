/** @odoo-module **/

import {jsonrpc} from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ResReferences = publicWidget.Widget.extend({
    selector: ".references",

    /**
     * @override
     */
    async start() {
        // Marking the function as async
        await this._super.apply(this, arguments);

        var $refHtml = this.$el.find("#res-references-row");

        if ($refHtml.length) {
            // Ensure the element exists
            try {
                const data = await jsonrpc("/get_references/", {});

                let html = "";
                data.forEach((reference) => {
                    let url = reference.link || "#";

                    if (url && !/^https?:\/\//i.test(url)) {
                        url = "https://" + url;
                    }
                    html += `<div class="pt16 pb16 o_colored_level col-lg-2">
                                <a href="${url}" target="_blank" style="text-decoration:none;">
                                    <div class="img img-fluid mx-auto" style="display: flex; justify-content: center; align-items: center; height: 100%;  /* tai mikä tahansa korkeus */">
                                        <img class="img img-fluid mx-auto" src="data:image/png;base64,${reference.image}"/>
                                    </div>
                                </a>
                            </div>`;
                });

                // Set innerHTML properly
                $refHtml.html(html);
            } catch (error) {
                console.error("Error fetching team data:", error);
            }
        }
    },
});
