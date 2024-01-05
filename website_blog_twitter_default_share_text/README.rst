.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================================
Website Blog: Customizable Twitter Default Share Text
=====================================================

* Enables you to configure the standard hardcoded "Amazing blog article: %s! Check it live: %s" text that is suggested
  when a user shares a Blog Post to Twitter / X.


Configuration
=============
* Set the new text in Website settings. Note that it has two "%s" placeholders, both of which are required. 
  The first one will be filled with the blog post title, the second one with the blog post URL.

  * If you have a multi-website Odoo, configure the text for all websites.

* Note: the Customize -> Show Sidebar needs to be toggled on in Website frontend for the module to have any effect. 

Usage
=====
* Click the Twitter/X share icon in the blog post sidebar. The default text is suggested but is changeable by the user.

Known issues / Roadmap
======================
* Consider having the configuration affect also Website Builder's "Inner Content / Share" widget's functionality (in core
  the two sharing methods are handled separately)
* Consider making the text translatable

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
