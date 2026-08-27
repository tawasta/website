.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
Web Editor: FontAwesome 6 Compatibility
=========================================

When ``base_fontawesome`` provides FontAwesome >= 6 (which defines icon
glyphs via a ``--fa: "\fXXX";`` custom property on the plain class
selector instead of a ``content: "\fXXX";`` declaration on a
``::before``/``:before`` selector), the web editor's own icon detection
code (``web_editor``'s ``fonts.js``) can no longer find any icons:

- The "Icons" tab in the media dialog shows no FontAwesome icons.
- Converting icons to images for outgoing HTML emails
  (``convert_inline.js``'s ``fontToImg``, used by mass mailing) breaks.

This module patches ``fonts.js``'s icon detection to also recognize the
FontAwesome >= 6 selector/declaration shape, normalizing it back into the
older ``content: "\fXXX";`` shape so every existing consumer of this data
keeps working unmodified.

Configuration
=============
\-

Usage
=====
Install this module alongside ``base_fontawesome`` when it provides
FontAwesome >= 6. No configuration needed.

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
