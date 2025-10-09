.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
User Role Switcher
==================

This module extends Odoo's multi-role functionality by allowing a user 
to **switch their active role** at runtime. It ensures that rights and 
groups are consistently updated based on the selected role, while 
maintaining strong security restrictions.

Key Features
============

* Define **Allowed Roles** per user.
* Users can switch their **active role** (`current_role_id`) 
  from the **portal dropdown** or their profile.
* Automatically updates `role_line_ids` and user groups 
  via Odoo core role logic.
* Security rules:
  
  - Only the logged-in user can change their own role.
  - Superuser (admin, `base.user_root`) cannot switch roles.
  - Roles outside the configured `allowed_role_ids` are rejected.
  - System-critical groups (``base.group_no_one``, ``base.group_system``) are protected.

Configuration
=============
No special configuration required. After installing:

1. Go to **Settings → Users**.
2. Define *Allowed Roles* for a user.
3. The first allowed role is automatically applied if no current role is set.

Usage
=====

**Backend:**
- If `current_role_id` is empty, the user form shows the standard `role_line_ids` field.
- Once a role is selected, `Allowed Roles` and `Current Role` are displayed instead.

**Portal:**
- Users see a **Change Role** option in the dropdown menu.
- A modal popup lists all allowed roles, and the user can switch instantly.
- The page reloads with the updated rights.

**Special Use Case**
--------------------
This module is primarily intended for **special scenarios** where a single user 
needs to operate in two very distinct contexts:

* As a **portal user**.
* As a **restricted internal user** (e.g. with very limited access to backend models).

By enforcing **one active role at a time**, the module prevents mixing portal 
and internal permissions, which could otherwise create security risks or lead 
to confusing access rights.

Known issues / Roadmap
======================
There are no known issues with this module.

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
