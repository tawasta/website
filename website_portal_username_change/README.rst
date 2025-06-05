.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
Change Username Feature for Odoo Portal
=======================================

This module adds a feature to the Odoo portal that allows users to change their username directly from the frontend. The change is facilitated through a user-friendly modal interface and includes validation to ensure a smooth process.

* Features
   - Allows users to update their username from the portal.
   - Displays the current username in the modal.
   - Requires users to confirm the new username.
   - Prevents duplicate usernames.
   - Automatically logs out users after a successful update.
   - Provides real-time validation and error handling.


Configuration
=============
\-

Usage
=====
The user clicks the Change Username button.

A modal pops up displaying the current username and fields for entering a new username.

The user enters and confirms the new username.

If the input is valid, the username is updated in the system.

The user is logged out and redirected to the login page.

Any errors (e.g., username already taken) are displayed in a modal dialog.

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
