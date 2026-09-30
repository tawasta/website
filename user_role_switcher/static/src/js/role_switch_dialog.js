/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

export class RoleSwitchDialog extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.user = useService("user");
        this.title = _t("Select Active Role");
        this.state = useState({ roles: [], selectedRoleId: false });

        onWillStart(async () => {
            const lines = await this.orm.searchRead(
                "res.users.allowed.role.line",
                [["user_id", "=", this.user.userId]],
                ["role_id"]
            );
            this.state.roles = lines.map((line) => ({
                id: line.role_id[0],
                name: line.role_id[1],
            }));

            const [userData] = await this.orm.read(
                "res.users",
                [this.user.userId],
                ["current_role_id"]
            );
            this.state.selectedRoleId = userData.current_role_id
                ? userData.current_role_id[0]
                : this.state.roles[0] && this.state.roles[0].id;
        });
    }

    onRoleChange(ev) {
        this.state.selectedRoleId = parseInt(ev.target.value, 10);
    }

    async onSave() {
        await this.rpc("/user_role_switcher/switch", {
            role_id: this.state.selectedRoleId,
        });
        this.props.close();
        browser.location.reload();
    }
}
RoleSwitchDialog.template = "user_role_switcher.RoleSwitchDialog";
RoleSwitchDialog.components = { Dialog };
RoleSwitchDialog.props = { close: Function };
