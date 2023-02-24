.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Website Kanban Board
====================
This module adds the possibility to create kanban board on a website/portal page.
You can use it like this:

.. code-block:: qweb

    <t t-call="website_skills_qualification.kanban_board">
        <t t-set="objects" t-value="<objects>"/>
        <t t-set="stages" t-value="<stages>"/>
    </t>

where **objects** are the records that are dropped into board (cards) and **stages** are the columns of the board.

Features
--------
\-


Installation
============

Install the module from Apps -> Website Kanban Board

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
* Aleksi Savijoki <aleksi.savijoki@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd..
