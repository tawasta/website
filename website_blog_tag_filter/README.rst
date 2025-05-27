.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Blog Tag Filter
===============

This Odoo module enables filtering blog posts by tag, accessible via `/tag/<id>` route.

Features
--------

- New public routes: `/tag/<tag_id>` and `/tag/<tag_id>/page/<page>`
- Fully compatible with Odoo's Website Blog module
- Uses Odoo's built-in `portal_pager` for pagination
- Integrates seamlessly with blog views: list/card layout, sidebar, teaser, cover image
- No core overrides or external dependencies


Configuration
=============
No special configuration is required. Once installed, the `/tag/<id>` route will automatically display posts associated with that tag.

Usage
=====
1. Navigate to `/tag/<tag_id>` (e.g., `/tag/3`)
2. You’ll see a list of all blog posts tagged with the given tag
3. If there are more than 10 posts, pagination will appear
4. The tag name is displayed in the header as: `Posts tagged with "TagName"`

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

-  Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

Futural Oy
