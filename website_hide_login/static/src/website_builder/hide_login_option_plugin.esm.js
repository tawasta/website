import {BaseOptionComponent} from "@html_builder/core/utils";
import {Plugin} from "@html_editor/plugin";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";

export class HideLoginOption extends BaseOptionComponent {
    static template = "website_hide_login.HideLoginOption";
    static selector = "main:has(.oe_website_login_container)";
    static title = _t("Login Page");
    static groups = ["website.group_website_designer"];
    static editableOnly = false;
}

export class HideLoginOptionPlugin extends Plugin {
    static id = "hideLoginOption";
    resources = {
        builder_options: [HideLoginOption],
    };
}

registry.category("website-plugins").add(HideLoginOptionPlugin.id, HideLoginOptionPlugin);
