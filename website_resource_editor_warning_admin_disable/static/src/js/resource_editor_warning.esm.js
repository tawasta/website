/** @odoo-module */

import { session } from "@web/session";

document.addEventListener('DOMContentLoaded', () => {
    if(session.is_admin === true || session.is_system === true) {
        window.localStorage.setItem("website.ace.doNotShowWarning", "true");
    }
});
