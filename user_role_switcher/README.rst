.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
User Role Switcher
==================

Switch your **active user role** at runtime while keeping security tight
and Odoo core role logic in sync. This module lets administrators define
*Allowed Roles* per user and allows end-users to switch their current
role from the portal header (dropdown + modal) or from their profile.

Key Features
============

* Define **Allowed Roles** per user, with optional company preference.
* Users can switch their **active role** (``current_role_id``)
  from the **portal dropdown** or their **user form**.
* Automatically updates ``role_line_ids`` and user groups
  using Odoo's core role logic (``base_user_role``).
* Strict security rules:

  - Only the logged-in user can change their own role.
  - Superuser (``base.user_root``) cannot switch roles.
  - Roles outside the configured *Allowed Roles* are rejected.
* Optional automatic **company switching** when a role has a company defined.

Configuration
=============
No special configuration is required. After installing:

1. Go to **Settings → Users**.
2. Under the **Roles** section:

   - Add one or more **Allowed Roles** for the user.
   - Optionally define a **Company** to activate when that role is chosen.

3. The first allowed role is automatically applied if no current role is set.

Usage
=====

**Backend:**

* The user form displays **Allowed Roles** and **Current Role** fields.
* Only roles marked as *Allow adding to Allowed Roles* can be selected.
* If a user's active role changes, the module:

  - Updates the Odoo core ``role_line_ids`` accordingly.
  - Refreshes user groups to match the selected role.
  - Switches company if configured on the allowed role line.

**Portal:**

* Users see a **Change Role** option in the portal dropdown.
* Clicking it opens a modal listing all allowed roles.
* Selecting a new role updates access rights instantly.
* The page reloads automatically with the new permissions.

**Example Flow:**

1. A user has two allowed roles: *Portal User* and *Internal Sales*.
2. While logged in as a portal user, they click **Change Role → Internal Sales**.
3. The module updates the backend role, reloads access rights, and optionally
   switches the company.

**Special Use Case**
--------------------
This module is primarily intended for cases where one user must operate in
two distinct contexts, such as:

* As a **portal user**.
* As a **restricted internal user**.

By enforcing **one active role at a time**, the module prevents
mixing portal and internal permissions, avoiding access confusion
and improving security.

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
