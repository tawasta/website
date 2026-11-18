.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Website: hide native login
==========================

Hide Odoo native login, but show oAuth-logins

* Hides the email and password fields and the "Log in" button
* Hides the "- or -" separator, "Reset Password" and "Don't have an account?"
* Hides "Use a Passkey" and the user switch ("Choose a user")
* Hiding is visual only: password login is still accepted by the server
* The native login is shown in debug mode (``/web/login?debug=1``)
* Each part can be toggled from the website editor (Customize)

Configuration
=============
\-

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

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy.
