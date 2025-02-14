/** @odoo-module **/

import {registry} from "@web/core/registry";
import publicWidget from "@web/legacy/js/public/public_widget";
import {jsonrpc} from "@web/core/network/rpc_service";

publicWidget.registry.ResTeams = publicWidget.Widget.extend({
    selector: ".team",

    /**
     * @override
     */
    async start() {
        // Marking the function as async
        await this._super.apply(this, arguments);

        var $teamHtml = this.$el.find("#res-team-row");

        if ($teamHtml.length) {
            // Ensure the element exists
            try {
                const data = await jsonrpc("/team/", {});

                let html = "";
                data.forEach((team) => {
                    html += `<div class="col-lg-4 col-md-6 mb-4 mb-lg-0 mt-3">
                        <div class="card shadow-lg border-0 h-100">
                            <div class="card-body p-4">
                                <img src="data:image/png;base64,${team.image}" alt="" class="img-fluid d-block mx-auto mb-3">
                                <div class="p-3">
                                    <h5 class="mb-0 text-center">${team.name}</h5>
                                    <p class="small text-muted text-center">${team.professional_title}</p>
                                    <p>${team.description}</p>
                                </div>
                            </div>
                        </div>
                    </div>`;
                });

                $teamHtml.html(html); // Set innerHTML properly
            } catch (error) {
                console.error("Error fetching team data:", error);
            }
        }
    },
});
