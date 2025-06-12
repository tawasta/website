.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Website Blog Tag Widget
=======================

This module adds a dynamic **tag cloud** snippet to the Odoo Website Builder using blog post tags. It is designed to integrate seamlessly with the `website_snippet_filter_core` for configurable dynamic filtering.


Features
========

- Adds a new visual snippet: **Tag Cloud**
- Tags are displayed as responsive badges using Bootstrap flex utilities
- Optional filtering of tags by `blog.tag.category`
- Customizable via the website editor UI

Configuration
=============

No additional configuration is required after installing the module.

Usage
=====

1. Go to **Website → Edit** mode.
2. Find the **"Tag Cloud"** snippet in the snippet sidebar under a custom panel.
3. Drag and drop the snippet onto the page.
4. Optionally, select categories from the snippet options to filter displayed tags.
5. Tags are clickable and link to `/blog/tag/<id>` URLs.


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
