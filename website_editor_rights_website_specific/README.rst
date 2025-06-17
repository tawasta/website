.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================
Website: Website Specific Editor Access Rights
==============================================

* In multiwebsite environment, specify for each website who can edit it
* Raises access error when clicking the following without access rights
  to the current website

  * Top left Editor
  * Top right Edit or Translate

Configuration
=============
* Create new user groups per website
* Go to website form, and set the 'Required Group Membership for Editing'
  to the new group
* Add the appropriate users to that group. Ensure they also have the 
  website editor or restricted editor access right.


Usage
=====
* Try to launch the website editor via frontend without access

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
