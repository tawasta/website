/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";

/**
 * Luodaan overlay-elementti dynaamisesti.
 */
let overlayElement = null;

export function showLoadingOverlay() {
    // Jos overlay on jo näkyvissä, ei lisätä uudelleen
    if (overlayElement) return;

    const message = _t("Loading, please wait...");

    overlayElement = document.createElement("div");
    overlayElement.id = "custom-loading-overlay";
    overlayElement.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;

    overlayElement.innerHTML = `
        <div style="text-align: center; color: white; font-family: sans-serif;">
            <div class="fa fa-spinner fa-spin" style="font-size: 3em; margin-bottom: 1em;"></div>
            <div style="font-size: 1.2em;">${message}</div>
        </div>
    `;

    document.body.appendChild(overlayElement);
}

export function hideLoadingOverlay() {
    if (overlayElement) {
        overlayElement.remove();
        overlayElement = null;
    }
}

// Varmistetaan että overlay ei jää päälle selaimen back/forward-navigaatiossa
window.addEventListener("pageshow", () => {
    hideLoadingOverlay();
});
