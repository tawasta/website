.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
Website Membership Fee Calculator Snippet
=========================================

* This module provides a website builder snippet for
  showing a membership fee calculator, so visitors can see their
  costs before joining.
* Since every organization has their different fee calculation logic,
  this module only provides the widget, but the calculation needs
  to happen in a separate, organization-based module.

  * To achieve this, inherit the controller's 
    calculate_website_membership_fee() function in your custom module.


Configuration
=============
* None needed

Usage
=====
* Drag and drop the Membership Fee Calculator widget, located in Dynamic Content,
  to website with the editor.
* The suggested label says 'Annual Turnover', but if the fees are based on some
  other metric, just change it with the editor.

Known issues / Roadmap
======================
* Consider supporting multiple separate calculations if there are e.g.
  different tiers of membership with different pricing. This would allow
  showing multiple calculator snippets.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/web/image/website/1/logo/Futural
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
