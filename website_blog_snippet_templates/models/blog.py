import html
import re

from lxml import html as lxml_html

from odoo import api, models


class BlogPost(models.Model):
    _inherit = "blog.post"

    @api.depends("content", "teaser_manual")
    def _compute_teaser(self):
        for blog_post in self:
            if blog_post.teaser_manual:
                blog_post.teaser = blog_post.teaser_manual
                continue

            document = lxml_html.fromstring(blog_post.content or "<div></div>")

            content = " ".join(document.itertext())
            content = html.unescape(content)
            content = re.sub(r"\s+", " ", content).strip()
            content = re.sub(r"\s+([,.!?;:])", r"\1", content)
            content = re.sub(r"([,;:])(?=\S)", r"\1 ", content)
            blog_post.teaser = content[:200].strip() + "..."
