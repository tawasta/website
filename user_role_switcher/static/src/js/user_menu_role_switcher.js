/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { RoleSwitchDialog } from "./role_switch_dialog";

function changeRoleItem(env) {
    return {
        type: "item",
        id: "change_role",
        description: _t("Change Role"),
        hide: !session.user_role_switcher_multi_role,
        callback: () => {
            env.services.dialog.add(RoleSwitchDialog);
        },
        sequence: 45,
    };
}

registry.category("user_menuitems").add("change_role", changeRoleItem);
