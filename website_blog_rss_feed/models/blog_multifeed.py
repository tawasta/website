from werkzeug import urls

from odoo import api, fields, models


class WebsiteBlogMultifeed(models.Model):
    # 1. Private attributes
    _name = "blog.multifeed"
    _description = "Blog RSS Multifeed"
    _order = "name"

    # 2. Fields declaration
    @api.model
    def _get_lang(self):
        return self.env["res.lang"].get_installed()

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    feed_url = fields.Char("Feed URL", readonly=1, compute="_compute_feed_url")
    lang = fields.Selection(
        required=True,
        selection=_get_lang,
        string="Language",
        help="Posts will be shown in this language in the RSS feed",
    )
    blog_ids = fields.Many2many(
        "blog.blog",
        string="Blogs",
        help="Blogs to include into this multifeed",
        index=True,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_feed_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for feed in self:
            feed.feed_url = urls.url_join(base_url, "/feed/%s" % feed.id)

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
