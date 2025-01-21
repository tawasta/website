##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "Website auth signup recaptcha (DEPRECATED)",
    "version": "17.0.1.0.0",
    "category": "Website",
    "summary": "Recaptcha functionality for website signup (deprecated)",
    "website": "https://gitlab.com/tawasta/odoo/website",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": ["auth_signup", "recaptcha_v2"],
    "data": ["views/auth_signup_login_templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "/website_auth_signup_recaptcha/static/src/js/signup.esm.js",
            "/website_auth_signup_recaptcha/static/src/js/reset.esm.js",
            "https://www.google.com/recaptcha/api.js",
        ],
    },
}
