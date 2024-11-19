.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
Website: Limit Editing Rights by Record Type (base)
===================================================

* Base functionality for allowing users to edit only certain types of website pages
* You'll likely want install also the record type specific modules for the 
  actual limiting of editing to e.g. event and/or eLearning related content
* Also grants rights to translate the related terms in frontend, without allowing
  translating e.g. headers and footers

Configuration
=============
* Add the users of your choice to the new "Website: Limit Editing Rights by Record Type (base)"
  group. They also get auto-added to the core "Restricted Editor" group. Ensure they are not
  in the "Editor and Designer" group.

Usage
=====
* In frontend try to launch the editor or translation view with an user that is in the new group, and you will get an
  access denied error for any page's editor.
* You can install the related event/eLearning modules that will whitelist editing for their content types

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
