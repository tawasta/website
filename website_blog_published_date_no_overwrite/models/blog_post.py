from odoo import models

# Keys the "Publish"/"Unpublish" action menu, the form/kanban switch and the
# frontend publish button write - and nothing else.
PUBLISH_TOGGLE_KEYS = {"is_published", "website_published"}


class BlogPost(models.Model):
    _inherit = "blog.post"

    def write(self, vals):
        # Only step in when the write is *exactly* a publish toggle. Any richer
        # write (a form save, an import, an explicit published_date, ...) keeps
        # standard Odoo behaviour untouched.
        is_publish_toggle = set(vals).issubset(PUBLISH_TOGGLE_KEYS) and any(
            vals.get(key) for key in PUBLISH_TOGGLE_KEYS
        )
        if not is_publish_toggle:
            return super().write(vals)

        # Core blog.post.write() stamps published_date = now() on publish
        # whenever the current value is empty or in the past, which destroys a
        # published_date imported from an external system. Pass the existing
        # value back explicitly so core skips its auto-stamp; posts without a
        # published_date still get one on publish.
        result = True
        keep_date = self.filtered("published_date")
        for post in keep_date:
            result &= super(BlogPost, post).write(
                dict(vals, published_date=post.published_date)
            )
        rest = self - keep_date
        if rest:
            result &= super(BlogPost, rest).write(vals)
        return result
