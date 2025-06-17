.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Signup url override
===================

This module fixes an issue where the generated signup URL can have the wrong domain,
especially when accessed via reverse proxies or multiple domain aliases.

It uses the `Referer` HTTP header as a trusted source to replace the domain
in the generated signup URL in reset password context (`/reset_password`),
to ensure the resulting link points to the correct domain for the user.

Configuration
=============
No configuration needed.

Usage
=====
1. Install the module
2. When users reset their password, the signup URL will now reflect the correct domain (based on the HTTP referer)

Known issues / Roadmap
======================


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
