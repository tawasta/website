/* eslint-disable no-unused-vars */
odoo.define("website_team_snippet.team", function (require) {
    "use strict";

    var core = require("web.core");
    var publicWidget = require("web.public.widget");
    publicWidget.registry.ResTeams = publicWidget.Widget.extend({
        selector: ".team",
        start() {
            const teamRow = this.el.querySelector("#res-team-row");

            if (teamRow) {
                this._rpc({
                    route: "/team/",
                    params: {},
                }).then((data) => {
                    let html = ``;
                    data.forEach((team) => {
                        html += `<div class="col-lg-4 col-md-6 mb-4 mb-lg-0 mt-3">
                        <div class="card rounded shadow">
        <div class="card-body p-4"><img src="data:image/png;base64,${team.image}" alt="" class="img-fluid d-block mx-auto mb-3">
          <div class="p-3">
            <h5 class="mb-0">${team.name}</h5>
            <p class="small text-muted">${team.professional_title}</p>
            <p>${team.description}</p>
          </div>
          </DIV>
        </div>
    </div>`;
                    });
                    teamRow.innerHTML = html;
                });
            }
        },
    });
});
