.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=============================
Website auth signup recaptcha
=============================
* This module integrates Google reCAPTCHA into the signup and reset password forms of the Odoo Website module to enhance security and prevent bot submissions.

Configuration
=============
* The `recaptcha_v2` module automatically adds the required fields for the Site Key and Secret Key to the **Website Settings** in Odoo:

Usage
=====
1. **Signup Form**:
   - The reCAPTCHA widget is automatically rendered in the signup form.
   - If reCAPTCHA verification fails, the form will not be submitted, and an error message will be displayed.

2. **Reset Password Form**:
   - The reCAPTCHA widget is added to the reset password form.
   - Verification is required before the form submission proceeds.

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
