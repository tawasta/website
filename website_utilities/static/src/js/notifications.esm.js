/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";

let container = null;

const TYPE_CONFIG = {
    info: {color: "#007bff", iconClass: "fa fa-info-circle"},
    success: {color: "#28a745", iconClass: "fa fa-check-circle"},
    warning: {color: "#ffc107", iconClass: "fa fa-exclamation-triangle"},
    error: {color: "#dc3545", iconClass: "fa fa-times-circle"},
};

/**
 * Näyttää toast-notifikaation.
 *
 * @param {Object} opts - Asetukset
 * @param {String} [opts.title=_t("Notice")] - Otsikko
 * @param {String} opts.message - Viesti (pakollinen)
 * @param {'info'|'success'|'warning'|'error'} [opts.type='info'] - Tyyppi
 * @param {Number} [opts.duration=5000] - Näyttöaika millisekunteina
 * @param {Boolean} [opts.dismissible=true] - Voiko sulkea manuaalisesti
 */
export function showNotification({
    title = _t("Notice"),
    message,
    type = "info",
    duration = 5000,
    dismissible = true,
} = {}) {
    if (!message) {
        console.warn("Notification message is required");
        return;
    }

    if (!container) {
        container = document.createElement("div");
        container.id = "custom-toast-container";
        container.setAttribute("aria-live", "polite");
        container.setAttribute("role", "region");
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 90vw;
            max-height: 70vh;
            overflow-y: auto;
            z-index: 9999;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        `;
        document.body.appendChild(container);
    }

    const {color, iconClass} = TYPE_CONFIG[type] || TYPE_CONFIG.info;

    const toast = document.createElement("div");
    toast.className = `custom-toast custom-toast-${type}`;
    toast.setAttribute("role", "alert");
    toast.setAttribute("tabindex", "0");
    toast.style.cssText = `
        background: white;
        border-left: 6px solid ${color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        padding: 14px 18px;
        min-width: 260px;
        max-width: 400px;
        border-radius: 8px;
        color: #333;
        display: flex;
        align-items: center;
        gap: 12px;
        animation: toastFadeIn 0.35s ease forwards;
        position: relative;
        user-select: none;
    `;

    toast.innerHTML = `
        <i class="${iconClass}" aria-hidden="true" style="font-size: 1.5em; line-height: 1; color: ${color};"></i>
        <div style="flex: 1;">
            <strong style="display:block; margin-bottom:4px;">${title}</strong>
            <div style="line-height: 1.3;">${message}</div>
        </div>
    `;

    // Define first -> no-use-before-define fixed
    const dismissToast = (element, timeoutId) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        element.style.animation = "toastFadeOut 0.35s ease forwards";
        element.setAttribute("aria-hidden", "true");
        element.removeAttribute("role");
        element.removeAttribute("tabindex");

        element.addEventListener(
            "animationend",
            () => {
                element.remove();
                if (container && container.children.length === 0) {
                    container.remove();
                    container = null;
                }
            },
            {once: true}
        );
    };

    let timeoutId = null;

    if (dismissible) {
        const btn = document.createElement("button");
        btn.setAttribute("aria-label", _t("Close notification"));
        btn.type = "button";
        btn.style.cssText = `
            background: transparent;
            border: none;
            color: #888;
            font-size: 1.2rem;
            cursor: pointer;
            padding: 0;
            line-height: 1;
            margin-left: 12px;
            align-self: start;
            user-select: none;
            transition: color 0.2s ease;
        `;
        btn.innerHTML = "&times;";
        btn.onclick = () => dismissToast(toast, timeoutId);
        btn.onkeydown = (ev) => {
            if (ev.key === "Enter" || ev.key === " ") {
                ev.preventDefault();
                dismissToast(toast, timeoutId);
            }
        };
        toast.appendChild(btn);
    }

    container.appendChild(toast);
    toast.focus();

    timeoutId = window.setTimeout(() => {
        dismissToast(toast, timeoutId);
    }, duration);
}

if (!document.getElementById("custom-toast-styles")) {
    const style = document.createElement("style");
    style.id = "custom-toast-styles";
    style.textContent = `
        @keyframes toastFadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes toastFadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(20px); }
        }
    `;
    document.head.appendChild(style);
}
