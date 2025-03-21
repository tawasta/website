.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Website Banner
==============
This module provides a dynamic and responsive banner for displaying advertisements on Odoo websites.  
It fetches and displays a random active advertisement from a selected category, tracks impressions and clicks, and supports time-based display settings.


Configuration
=============

1. Go to **Website > Configuration > Advertisements**.
2. Create one or more **Advertisement Categories**.
3. Create **Advertisements** and configure:
   - Name
   - Category
   - Start and End Date (validity period)
   - URL (target link)
   - Image (ad content)
   - Active status

Usage
=====
1. In the Website Builder, drag and drop the **Wide Banner** snippet onto your page.
2. Set the `data-category-id` attribute in the snippet's HTML to the desired ad category ID.
3. The banner will automatically load a random ad from that category using JSON-RPC.
4. Banner clicks redirect users to the ad’s target URL, and view/click counts are tracked.


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
