from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    read_blog_post_ids = fields.Many2many(
        string="Read blog posts",
        comodel_name="blog.post",
        relation="read_blog_post_rel",
        readonly=True,
    )

    read_free_blog_post_ids = fields.Many2many(
        string="Free tier read blog posts",
        comodel_name="blog.post",
        relation="read_free_blog_post_rel",
        readonly=True,
    )

    def _cron_reset_read_free_blog_post_ids(self):
        records = self.search([])
        records.reset_read_free_blog_post_ids()

    def reset_read_free_blog_post_ids(self):
        # Reset free tier blog posts
        self.write({"read_free_blog_post_ids": False})
