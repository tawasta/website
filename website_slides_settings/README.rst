.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Website Slides Settings
=======================
* Toggleable Settings under website customize menu:
  - In slide

  - In slide page
    - Hide "search courses" textbox
    - Hide Breadcrumbs
    - Hide Tab Navigation
    - Add option to slide page to disable fullscreen by default # In progress

  - In slide homepage


  - TODO
    - Hide "search courses" textbox in slide homepage header
    - Hide Breadcrumps in slide homepage header
    - Hide All views on slide
    - Hide Total views on slide
    - Hide Public views on slide
    - Hide Member views on slide
    - Hide Share tab on slide
    - Hide User Profile on slide homepage
    - Hide User Achievements on slide homepage
    - Hide "Share" button in slide homepage header
    - Hide the tablist element in slides homepage header (the one that contains e.g. items "Course" and "Reviews"
    - Hide the 'Search in content' search box
    - Hide the 'Order by' dropdown of the content search results
    * Add banner image from backend to '/slides/all' view. This fixes a bug in Odoo editor
  which does not allow changing the banner.

Configuration
=============
* Set the slides banner image from backend website Settings
* Toggle other settings via website builder as needed

Usage
=====
\-

Known issues / Roadmap
======================
* Add banner image from backend to '/slides/all' view. This fixes a bug in Odoo editor
  which does not allow changing the banner. NOTE: Remove this in migration as this is
  fixed upstream. Keep for v14 as deprecated feature as removing field is risky.

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>
* Joona Isoaho <joona.isoaho@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
