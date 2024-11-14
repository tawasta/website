##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2024 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    "name": "Website: Limit Editing Rights by Record Type (base)",
    "summary": "Base functionality for allowing users to edit only certain types of website pages",
    "version": "17.0.1.1.0",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/website",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website", "web_editor"],
    "data": ["security/res_groups.xml"],
    "assets": {
        "website.assets_editor": [
            # These need to be included or backend wysiwyg editor won't load
            "web_editor/static/src/js/editor/toolbar.js",
            "web_editor/static/src/xml/*",
            # Needed for the actual frontend wysiwyg functionality
            "web/static/src/legacy/*",
            "web/static/src/legacy/js/core/widget",
            "web/static/src/legacy/js/core/*",
            "web_editor/static/src/js/editor/*",
            "web_editor/static/src/js/editor/odoo-editor/*",
            "web_editor/static/src/js/editor/odoo-editor/src/*",
            "web_editor/static/src/js/editor/odoo-editor/src/utils/*",
            "web_editor/static/src/js/editor/odoo-editor/src/commands/*",
            "web_editor/static/src/js/editor/odoo-editor/src/powerbox/*",
            "web_editor/static/src/js/editor/odoo-editor/src/tablepicker/*",
            "web_editor/static/src/js/wysiwyg/*",
            "web_editor/static/src/js/wysiwyg/widgets/*",
            "website/static/src/components/wysiwyg_adapter/wysiwyg_adapter.js",
            "website_limit_editing_rights_by_record_type_base/static/src/js/systray_translate_website.esm.js",
            "website_limit_editing_rights_by_record_type_base/static/src/js/systray_edit_website.esm.js",
            "website_limit_editing_rights_by_record_type_base/static/src/js/wysiwyg_adapter.esm.js",
        ],
    },
}
