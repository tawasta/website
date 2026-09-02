from datetime import datetime, timedelta

from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPublishedDateNoOverwrite(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blog = cls.env["blog.blog"].create({"name": "Test Blog"})
        cls.past_date = datetime(2020, 1, 15, 8, 30, 0)

    def _new_post(self, **vals):
        values = {
            "name": "Test Post",
            "blog_id": self.blog.id,
            "is_published": False,
        }
        values.update(vals)
        return self.env["blog.post"].create(values)

    def test_preserve_existing_date_on_publish(self):
        post = self._new_post(published_date=self.past_date)
        post.write({"is_published": True})
        self.assertTrue(post.is_published)
        self.assertEqual(post.published_date, self.past_date)

    def test_preserve_existing_date_on_website_published(self):
        post = self._new_post(published_date=self.past_date)
        post.write({"website_published": True})
        self.assertTrue(post.website_published)
        self.assertEqual(post.published_date, self.past_date)

    def test_stamp_date_when_missing(self):
        post = self._new_post()
        self.assertFalse(post.published_date)
        before = fields.Datetime.now()
        post.write({"is_published": True})
        self.assertTrue(post.published_date)
        self.assertGreaterEqual(post.published_date, before - timedelta(seconds=5))

    def test_unpublish_still_clears_date(self):
        post = self._new_post(published_date=self.past_date)
        post.write({"is_published": True})
        post.write({"is_published": False})
        self.assertFalse(post.published_date)

    def test_explicit_date_wins(self):
        other_date = datetime(2021, 6, 1, 12, 0, 0)
        post = self._new_post(published_date=self.past_date)
        post.write({"is_published": True, "published_date": other_date})
        self.assertEqual(post.published_date, other_date)

    def test_non_toggle_write_keeps_core_behaviour(self):
        # Publishing bundled with other field changes is not a plain toggle,
        # so standard Odoo still overwrites the past date with "now".
        post = self._new_post(published_date=self.past_date)
        post.write({"is_published": True, "name": "Renamed"})
        self.assertGreater(post.published_date, self.past_date)
