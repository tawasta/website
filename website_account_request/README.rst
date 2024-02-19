.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Website account request Snippet
===============================

This module introduces a feature that allows users to request access to a demo Odoo system directly from the website. By filling out a simple form with their email address, users can submit a request to gain temporary access credentials. Upon submission, a notification is sent to the system administrator, and the user is provided with login details if an available demo account is found. This module streamlines the process of granting potential users a sneak peek into the system's functionalities, enhancing user engagement and interest.

For the administrator to ensure this feature functions correctly, several steps must be taken:

   -Configuration of Email Parameters: The administrator must ensure that the outgoing email server settings are correctly configured in Odoo. This is crucial for sending notifications to the system administrator and account request confirmations to users.

   -Demo Users Setup: The administrator should set up a predefined number of demo user accounts within the Odoo system. These accounts should have limited access rights, tailored to showcase the system's features without compromising security or data integrity.

   -Group Assignment: Ensure that the demo user accounts are assigned to a specific user group, like "Demo Users." This group's rights should be carefully configured to prevent unauthorized access to sensitive information or critical functionalities.

   -System Parameters: The administrator needs to define system parameters, such as the target email address for notifications (account_request.target_email) and the system URL (web.base.url). These parameters are used by the module to route information correctly.

Configuration
=============
\-

Usage
=====
\-

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
