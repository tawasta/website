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

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
