# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015- Oy Tawasta Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Website Futurality Theme',
    'category': 'Theme',
    'version': '0.1',
    'author': 'Oy Tawasta Technologies Ltd',
    'website': 'http://www.tawasta.fi',
    'depends': [
        'website',
        'website_sale',
    ],
    'description': '''
Website Futurality Theme
========================

Futurality theme for the website-module


Features
========
* Simplifies the website
* Adds some Futurality-colours
''',
    'data': [
        'views/style.xml',
        'views/contact.xml',
        'views/layout.xml',
        'views/sale_product.xml',
    ],
    'application': True,
}
