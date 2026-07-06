import {patch} from "@web/core/utils/patch";
import publicWidget from "@web/legacy/js/public/public_widget";

patch(publicWidget.registry.websiteSlidesCourseSlidesList.prototype, {
  /**
   * Override _updateHref to inject custom logic
   */
  _updateHref() {
    // Kutsu alkuperäistä metodia (jos haluat säilyttää sen muun toiminnallisuuden)
    this._super.apply(this, arguments);

    // Oma mukautettu logiikka:
    this.$(".o_wslides_js_slides_list_slide_link").each(function () {
      // Lisää "fullscreen=1" vain jos elementillä EI ole tiettyä luokkaa
      if (!$(this).hasClass("o_wslides_js_slides_list_slide_link_disable")) {
        const href = $(this).attr("href");
        const operator = href.includes("?") ? "&" : "?";
        $(this).attr("href", href + operator + "fullscreen=1");
      }
    });
  },
});
