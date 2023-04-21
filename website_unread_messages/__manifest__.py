##############################################################################
#
#    Author: Tawasta
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Website Unread Messages",
    "summary": "Unread messages for website",
    "version": "12.0.3.1.0",
    "category": "Website",
    "website": "https://github.com/Tawasta/website",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_messages_base"],
    "data": [
        "data/website_unread_messages_data.xml",
        "views/res_config_settings_views.xml",
        "views/website_unread_messages_static.xml",
        "views/website_unread_message.xml",
    ],
}
