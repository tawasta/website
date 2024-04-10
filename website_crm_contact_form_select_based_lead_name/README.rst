.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================================
Website CRM: Selection-based Contact Form Opportunity Subject
=============================================================

* By default, when you configure the contact form to create
  an Opportunity, the opportunity name/subject is typed in by the sender
  on the form
* In some cases you would want to limit the values to be based
  on a selection list instead.
* This module allows you to achieve this with just the website builder.

Configuration
=============
* Install the module
* Create a contact form and configure it to create an Opportunity.
* The default Subject field cannot be removed, so configure its visibility
  to "Hidden"
* Add the field "Name from Preselected Options" to the form and give it
  the label "Subject", and make the field Required.
* Save the form

Usage
=====
* Make a form submission from the new form. The selection field value
  becomes the Opportunity's subject.
* Opportunities created from backend remain unaffected.

Known issues / Roadmap
======================
* The model contains certain subjects such as "Resale" and "Returns". 
  If you need others, inherit and override as needed

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
