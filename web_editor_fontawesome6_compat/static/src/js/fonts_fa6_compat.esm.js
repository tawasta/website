/** @odoo-module **/

import {fonts} from "@web_editor/js/wysiwyg/fonts";
import {patch} from "@web/core/utils/patch";

patch(fonts, {
    // FontAwesome >= 6 (base_fontawesome) defines the icon glyph as a CSS
    // custom property (--fa: "\fXXX";) directly on the class selector,
    // with no ::before/:before suffix and no "content:" declaration at
    // all - unlike the older format this parser was written for.
    // Relaxed to match both the old and the new selector shape.
    fontIcons: [{base: "fa", parser: /\.(fa-(?:\w|-)+)(?:::?before)?/i}],

    getCssSelectors(filter) {
        if (this.cacheCssSelectors[filter]) {
            return this.cacheCssSelectors[filter];
        }
        this.cacheCssSelectors[filter] = [];
        const sheets = document.styleSheets;
        for (let i = 0; i < sheets.length; i++) {
            let rules = null;
            try {
                // Try...catch because Firefox not able to enumerate
                // document.styleSheets[].cssRules[] for cross-domain
                // stylesheets.
                rules = sheets[i].rules || sheets[i].cssRules;
            } catch {
                continue;
            }
            if (!rules) {
                continue;
            }

            for (let r = 0; r < rules.length; r++) {
                const selectorText = rules[r].selectorText;
                if (!selectorText) {
                    continue;
                }
                let cssText = rules[r].cssText;

                // FontAwesome >= 6 rule: normalize "--fa: "X";" back into
                // an equivalent "content: "X";" declaration, so every
                // existing consumer of this data (IconSelector,
                // convert_inline.js's fontToImg used when sending mass
                // mailings) keeps working unmodified.
                if (!/content\s*:/.test(cssText)) {
                    const faVarMatch = cssText.match(/--fa:\s*(["'][^"']*["'])/);
                    if (!faVarMatch) {
                        continue;
                    }
                    cssText = cssText.replace(/\{/, `{ content: ${faVarMatch[1]};`);
                }

                const selectors = selectorText.split(/\s*,\s*/);
                let data = null;
                for (let s = 0; s < selectors.length; s++) {
                    const match = selectors[s].trim().match(filter);
                    if (!match) {
                        continue;
                    }
                    if (!data) {
                        data = {
                            selector: match[0],
                            css: cssText.replace(/(^.*\{\s*)|(\s*\}\s*$)/g, ""),
                            names: [match[1]],
                        };
                    } else {
                        data.selector += ", " + match[0];
                        data.names.push(match[1]);
                    }
                }
                if (data) {
                    this.cacheCssSelectors[filter].push(data);
                }
            }
        }
        return this.cacheCssSelectors[filter];
    },
});
