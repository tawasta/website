/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";

/**
 * Tarkistaa tiedostojen koot ja lisää tiedon info_div:iin.
 * Täysin identtinen alkuperäisen odoo.define-version kanssa.
 *
 * @param {HTMLElement} el - Input-elementti, jossa tiedostot
 * @param {HTMLElement} info_div - Kohdedivi viestien näyttöön
 * @returns {boolean} - Palauttaa true, jos tiedosto on liian suuri
 */
export function checkFileSizes(el, info_div) {
    const files = $(el).prop("files");
    const maxSize = $(el).data("maxsize"); // haetaan kuten alkuperäisessä
    let size = "";
    let elements = "";
    let fileTooBig = false;

    const fileCount = files.length.toString() + _t(" file(s) selected:");
    const fileNameLabel = _t("File name: ");
    const fileSizeLabel = _t("File size: ");
    const fileTooBigLabel = _t("File size too big! Max size for file is ") + maxSize + "MB";

    $(info_div).addClass("d-none");

    elements += "<p>" + fileCount + "</p><p id='file_sizes'>";

    for (let i = 0; i < files.length; ++i) {
        const file = files[i];

        if (file.size > 1024 * 1024) {
            size = (Math.round((file.size * 10) / (1000 * 1000)) / 10).toString() + "MB";
        } else {
            size = (Math.round((file.size * 10) / 1000) / 10).toString() + "KB";
        }

        if (file.size > maxSize * 1000 * 1000) {
            fileTooBig = true;
            elements += "<strong>" + fileTooBigLabel + "</strong><br/>";
            elements += fileNameLabel + file.name + ", " + fileSizeLabel + size + "<br/><br/>";
        } else {
            elements += fileNameLabel + file.name + ", " + fileSizeLabel + size + "<br/>";
        }
    }

    elements += "</p>";

    if (fileTooBig) {
        $(info_div).removeClass("d-none alert-info").addClass("alert-danger");
    } else {
        $(info_div).removeClass("d-none alert-danger").addClass("alert-info");
    }

    $(info_div).html(elements);

    return fileTooBig;
}

export default {
    checkFileSizes,
};
