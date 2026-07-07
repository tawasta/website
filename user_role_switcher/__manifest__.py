##############################################################################
#
#    Author: Futural Oy
#    Copyright 2019- Futural Oy (https://futural.fi)
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
    "name": "User Role Switcher",
    "summary": "Let users switch their active res.users.role at runtime",
    "version": "17.0.1.0.0",
    "category": "Web",
    "website": "https://github.com/tawasta/website",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "web",
        "portal",
        "base_user_role",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/user_role.xml",
    ],
}
