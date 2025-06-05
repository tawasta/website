.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

====================================
Website Snippet Filter Core Override
====================================
This Odoo module provides an extensible override for the `website.snippet.filter`
mechanism, allowing fine-grained control over domain construction when rendering
dynamic content blocks on a website.

It refactors the `_prepare_values` method and introduces clearly separated
domain-handling hooks:

* `_get_website_domain`
* `_get_company_domain`
* `_get_is_published_domain`

These allow other modules to selectively override logic (e.g. skip `company_id` filtering
for specific models)

Features
========

* Refactored `_prepare_values` for maintainability
* Clean separation of domain logic into reusable methods
* Safe and extensible design for inheriting modules

Configuration
=============

No configuration required.

Usage
=====
\-

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
