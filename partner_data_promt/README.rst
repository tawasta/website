.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

===================
Partner Data Prompt
===================
This module enables automatic prompting of missing partner data from portal users (customers) after login.
Administrators can define dynamic rules for which fields should be requested, and under what conditions.


Features
========

- Prompt portal users to complete missing partner fields
- Define dynamic rules based on partner field, requirement, and domain condition
- Fields supported:
  - char
  - integer
  - selection
  - many2one
  - many2many
  - date
- Respects interval setting to avoid repeated prompts
- Integrated with Bootstrap modal and Select2 (for dropdown fields)

Configuration
=============
1. Go to *Website > Data Prompt Rules*
2. Create a new rule:
   - **Field**: Select a field from `res.partner`
   - **Required**: Should the field be prompted if empty
   - **Condition Domain** *(optional)*: Odoo domain in Python format, for example:
     ::

         [('is_company', '=', True)]

   - **Prompt Text**: Custom explanation shown to the user for each field
3. Go to **Website Settings** and set **Data Prompt Interval (days)** to control how often the modal appears (default: 30 days)

Usage
=====
1. User logs into the website (portal)
2. System checks whether:
   - The configured interval since last prompt has passed
   - There are active prompt rules with missing values for this user
3. If applicable, a modal is shown requesting the user to fill in the missing data
4. Submitted data is saved directly to `res.partner`
5. Prompt timestamp (`data_check_date`) is updated

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

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
