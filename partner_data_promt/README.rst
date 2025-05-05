.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

===================
Partner Data Prompt
===================
This module enables automatic prompting of missing partner data from portal users (customers) after login.
Administrators can define dynamic rules for which partner fields should be requested, under which conditions, and how often.


Features
========

- Prompt portal users to fill in or confirm partner field values
- Dynamically show fields based on active rule definitions
- Respects an interval (in days) between prompts to avoid spamming users
- Full support for:
  - `char`
  - `integer`
  - `selection`
  - `many2one`
  - `many2many`
  - `date`
- Fully integrated with Bootstrap modal, Select2, and Tempus Dominus date picker
- User can confirm data is up to date even if no changes are made

Logic
=====
1. If there are **missing values** based on active rules and matching conditions →  
   🔹 Show only **those missing fields**

2. If **all fields are filled**, but **`data_check_date` is old** or not set →  
   🔹 Show **all active rules' fields**, **regardless of whether condition matches or not**,  
   🔹 Pre-fill all values for user to review and confirm

3. If all fields are filled **and** check date is recent →  
   🔹 No modal is shown

This logic ensures a balance between accuracy (prompting when needed) and avoiding annoyance (skipping when recently confirmed).


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
1. User logs in to portal
2. System checks:
   - Missing data (based on rules + conditions)
   - Last time user confirmed data (`data_check_date`)
3. If needed, modal is shown with required or reviewable fields
4. Submitted data is saved to `res.partner`
5. `data_check_date` is updated

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
