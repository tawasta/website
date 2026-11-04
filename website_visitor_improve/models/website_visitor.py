import logging
import threading

from psycopg2 import errors

from odoo import models
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


class WebsiteVisitor(models.Model):
    _inherit = "website.visitor"

    def _cron_unlink_old_visitors(self, batch_size=1000, limit=None):
        """Unlink inactive visitors (see '_inactive_visitors_domain' for
        details).

        Visitors were previously archived but we came to the conclusion that
        archived visitors have very little value and bloat the database for no
        reason.

        The visitors are deleted in small batches. Each batch is searched,
        locked and deleted right after one another, and committed before the
        next batch starts. This keeps the time window short in which another
        transaction (e.g. a login merging the visitor into a partner) can
        delete or change the same visitor and make the cleanup fail.
        """
        auto_commit = not getattr(threading.current_thread(), "testing", False)
        # Without an explicit limit, process one batch at most.
        remaining = limit or batch_size

        while remaining > 0:
            try:
                with self.env.cr.savepoint():
                    batch = self._lock_inactive_visitors(min(batch_size, remaining))
                    batch.unlink()
            except errors.SerializationFailure:
                # PostgreSQL refuses to touch a row that another transaction
                # has deleted or updated after our transaction started.
                # Nothing is lost: the remaining visitors are cleaned on the
                # next run.
                _logger.warning(
                    "Inactive visitor cleanup stopped by a concurrent change"
                )
                return
            if not batch:
                return
            remaining -= len(batch)
            if auto_commit:
                self.env.cr.commit()  # pylint: disable=invalid-commit

    def _lock_inactive_visitors(self, size):
        """Return up to `size` inactive visitors and lock them against other
        transactions until the next commit.

        - Visitors that another transaction is changing right now are skipped.
        - If a visitor was changed after our transaction started (e.g. the
          visitor came back to the website), PostgreSQL raises a
          SerializationFailure. The caller handles it, so an active visitor
          is never deleted.
        """
        visitor_ids = (
            self.sudo().search(self._inactive_visitors_domain(), limit=size).ids
        )
        if not visitor_ids:
            return self.browse()
        self.env.cr.execute(
            SQL(
                "SELECT id FROM %s WHERE id IN %s FOR UPDATE SKIP LOCKED",
                SQL.identifier(self._table),
                tuple(visitor_ids),
            )
        )
        return self.browse([row[0] for row in self.env.cr.fetchall()])
