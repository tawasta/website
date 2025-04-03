.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Website Banner
==============
This module provides a dynamic and responsive banner for displaying advertisements on Odoo websites.  
It fetches and displays a random **active** advertisement from a selected category, tracks **impressions** and **clicks**, and supports **time-based display conditions**.


Configuration
=============

1. Go to **Website > Configuration > Advertisements**.
2. Create one or more **Advertisement Categories**.
3. Create **Advertisements** and configure the following:
   - **Name**: Title of the ad.
   - **Category**: Category the ad belongs to.
   - **Start and End Date**: Validity period during which the ad is displayed.
   - **URL**: Target link the banner points to.
   - **Image**: Content shown in the banner.
   - **Active**: Only active ads will be shown.

Usage
=====
1. In the **Website Builder**, drag and drop the **Wide Banner** snippet onto your page.
2. Set the `data-category-id` attribute in the snippet’s HTML to the desired advertisement category ID.
3. The banner will automatically load a **random active ad** from the selected category using **JSON-RPC**.
4. Banner **views** and **clicks** are automatically tracked per advertisement.


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
