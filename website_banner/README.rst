.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Website Banner
==============
This module provides a dynamic and responsive banner for displaying advertisements on Odoo websites.
It fetches and displays one or more **random active advertisements** from selected **categories**, tracks **impressions** and **clicks**, and supports **time-based display conditions**.

Features
========
- Displays advertisements in a banner format
- **Supports multiple categories** using many2many selection
- Filters by date (start/end) and active status
- Tracks impressions and clicks via JSON-RPC
- Fully integrated into the Odoo website editor as a dynamic snippet

Configuration
=============

1. Go to **Website > Configuration > Advertisement Categories**.
2. Create one or more **Advertisement Categories**.
3. Go to **Website > Configuration > Advertisements** and configure each ad:
   - **Name**: Title of the ad
   - **Categories**: One or more categories the ad belongs to
   - **Start and End Date**: Visibility period
   - **Target URL**: Link the ad should open
   - **Image**: Ad content
   - **Active**: Only active ads are shown

Usage
=====

1. Open the **Website Builder**.
2. Drag and drop the **Advertisement Banner** snippet onto a page.
3. Use the **snippet options panel** to select one or more advertisement categories.
4. The banner will display a **random active advertisement** matching the selected categories.
5. All **views and clicks** are tracked automatically via backend RPC calls.



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
