.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================================
Website Blog: Don't Overwrite Published Date
============================================

* Helper module for situations where you mass import blog posts along with their
  publishing dates from an external system, but you want to publish them 
  manually in Odoo without losing the original publishing date info.
* If blog post already has a `published_date` and the post is unpublished, 
  publishing it will not overwrite it with current date. 
* Note that unpublishing a blog post will still clear the published date
  field as in Odoo core.
* The date is only kept when publishing via a plain publish toggle: the
  "Publish" action menu entry, the Published switch on the form/kanban, or
  the frontend Publish button. 
  
  * Saving the form with other changes at the
    same time, imports, and other writes keep standard Odoo behaviour.

Configuration
=============
* None needed

Usage
=====
* Just publish some imported blog posts via Blog Posts list -> Actions -> Publish. 
  Their published date will not get overwritten.
* The module has no use afterwards, you can uninstall it after the import/publish
  process has been completed.

Known issues / Roadmap
======================

\-

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
