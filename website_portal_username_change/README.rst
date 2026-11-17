.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Website Portal: Username Change Option
======================================

* Adds a "Change Username" button to the portal security page (/my/security).
  The button and the change are available to portal users only.
* The user enters and confirms the new username and their current password,
  and is logged out after the change. Every change is logged as an internal note on the user's contact.

Configuration
=============
* Optionally, in Settings > General Settings toggle the 
  "Update Contact Email on Portal Username Change" setting on (off by default)

  * When enabled, the new username is also written as the contact's email
    address, and it must be a valid email address.

Usage
=====
* Navigate to Portal > Security > Change Username.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
