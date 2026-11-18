.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================================================
Disable to create an account from login when 'Free sign up' is enabled
======================================================================

::

    This module is meant to be used together with some OAuth Authentication.
    For example if Google Authentication is used and website -module is
    installed, then 'Free sign up' is needed, but this module disabled to
    create accounts freely from login screen. Users need to use some form
    of authentication to login/sign up.

    The sign up page (/web/signup) requires a logged-in user. A visitor
    who opens it is redirected to the login page.

Configuration
=============
::

    Go to settings to activate 'Free sign up'. Then set up OAuth Authentication
    to login users.

Usage
=====
::

    After configuration the users only need to login.

Known issues / Roadmap
======================
::

    See if an installation have some modules installed which use web_auth_signup method.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Timo Talvitie <timo.talvitie@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy.
