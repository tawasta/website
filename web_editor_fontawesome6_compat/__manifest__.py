##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026- Futural Oy (https://futural.fi)
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
    "name": "Web Editor: FontAwesome 6 Compatibility",
    "summary": "Fix the web editor's icon picker and email icon conversion "
    "when base_fontawesome provides FontAwesome >= 6",
    "version": "17.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/tawasta/website",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["web_editor", "base_fontawesome"],
    "assets": {
        "web.assets_backend": [
            "web_editor_fontawesome6_compat/static/src/js/fonts_fa6_compat.esm.js",
        ],
        "web.assets_frontend": [
            "web_editor_fontawesome6_compat/static/src/js/fonts_fa6_compat.esm.js",
        ],
    },
}
