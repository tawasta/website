.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Website Visitor Cleanup Limit Fix
=================================

This module improves the default website visitor cleanup mechanism in Odoo by enforcing a safe search limit when removing inactive visitors.

By default, the cleanup process may attempt to process a large number of records at once. This module ensures that the cleanup is performed in controlled batches, preventing excessive memory usage and potential performance issues.

The module overrides the existing cron job behavior to:
- Enforce a search limit when fetching inactive visitors
- Search, lock and delete the visitors one batch at a time (100 visitors per batch, 500 per run)
- Skip visitors that another transaction is currently working on (``FOR UPDATE SKIP LOCKED``)
- Stop the run with a warning instead of failing when a visitor was deleted or updated concurrently,
  for example by a login merging the visitor into a partner. The remaining visitors are cleaned on the next run.
- Automatically commit transactions between batches (outside testing environments)

Configuration
=============

No additional configuration is required.

The module automatically updates the existing scheduled action responsible for cleaning up website visitors. The cron job will use the improved logic once the module is installed.

Usage
=====

The module works automatically in the background.

Once installed:
- The scheduled action for cleaning inactive website visitors will run as usual
- Cleanup will be performed in batches with a defined limit
- No manual interaction is needed

Known issues / Roadmap
======================

- No known issues at the moment
- Future improvements may include configurable batch size and limit via system settings

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