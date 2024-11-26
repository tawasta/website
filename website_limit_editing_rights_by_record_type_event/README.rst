.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================================
Website: Limit Editing Rights by Record Type (Events) (DEPRECATED)
==================================================================

* Allow users to edit their company's event related pages but prevent editing
  other types of pages (blogs, regular pages etc.)
* Deprecated and set as uninstallable: https://github.com/odoo/odoo/commit/5d717f3ff5ce83faf2ce12ef03942bb00684eb68 
  and other related changes to 17.0 core break this functionality, and also support similar functionality 
  for the Website Restricted Editor Group out of the box.

Configuration
=============
* Add the users of your choice to the new "Website: Limit Editing Rights by Record Type (events)"
  group

Usage
=====
* In frontend launch the editor. From non-event pages it will give an access denied error.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
