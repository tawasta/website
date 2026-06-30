##############################################################################
#
#    Author: Futural Oy
#    Copyright 2022- Futural Oy (https://futural.fi)
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
    "name": "Website References Snippet",
    "summary": "Snippet for showing e.g. company's clients on a web page",
    "version": "17.0.1.0.1",
    "category": "Website",
    "website": "https://github.com/tawasta/website",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website", "website_snippet_filter_core"],
    "data": [
        "security/ir.model.access.csv",
        "views/reference.xml",
        "data/snippet_filter.xml",
        "views/snippets/s_references.xml",
        "views/snippets/snippets.xml",
        "views/snippets/options.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_references_snippet/static/src/snippets/s_references/000.esm.js",
            "website_references_snippet/static/src/scss/s_references.scss",
        ],
        "website.assets_wysiwyg": [
            "website_references_snippet/static/src/snippets/s_references/options.esm.js",
        ],
    },
}
