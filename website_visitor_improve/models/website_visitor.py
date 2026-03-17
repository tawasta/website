import threading

from odoo import models
from odoo.tools import split_every


class WebsiteVisitor(models.Model):
    _inherit = "website.visitor"

    def _cron_unlink_old_visitors(self, batch_size=1000, limit=None):
        """Unlink inactive visitors (see '_inactive_visitors_domain' for
        details).

        Visitors were previously archived but we came to the conclusion that
        archived visitors have very little value and bloat the database for no
        reason.
        """
        auto_commit = not getattr(threading.current_thread(), "testing", False)
        visitor_model = self.env["website.visitor"]

        # Never perform an unlimited search by default.
        # If limit is not given, use batch_size as the search limit.
        search_limit = limit or batch_size

        for inactive_visitors_batch in split_every(
            batch_size,
            visitor_model.sudo()
            .search(
                self._inactive_visitors_domain(),
                limit=search_limit,
            )
            .ids,
            visitor_model.browse,
        ):
            inactive_visitors_batch.unlink()
            if auto_commit:
                self.env.cr.commit()  # pylint: disable=invalid-commit
