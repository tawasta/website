/** @odoo-module **/

import {jsonrpc} from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.MembershipFeeCalculator = publicWidget.Widget.extend({
    selector: ".s_membership_fee_calculator",
    events: {
        "click .mfc_calculate_btn": "_onClickCalculate",
        "keypress #calculator_fee_basis": "_onKeypressInput",
    },

    /**
     * Allow pressing Enter to trigger calculation.
     *
     * @param {*} ev event object
     */
    _onKeypressInput(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            this._onClickCalculate(ev);
        }
    },

    /**
     * Main handler: read the input, call the backend, show the result.
     *
     * @param {*} ev event object
     */
    async _onClickCalculate(ev) {
        ev.preventDefault();
        const inputEl = this.el.querySelector("#calculator_fee_basis");
        const resultEl = this.el.querySelector("#calculator_fee_result");

        // Comma to point
        const raw = (inputEl.value || "").replace(/,/g, ".");
        const feeBasis = parseFloat(raw);

        try {
            const result = await jsonrpc(
                "/website_membership_fee_calculator/calculate",
                {fee_basis: feeBasis}
            );
            resultEl.textContent = result.fee;
        } catch (err) {
            console.error("MembershipFeeCalculator error:", err);
        }
    },
});

export default publicWidget.registry.MembershipFeeCalculator;
