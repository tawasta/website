from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager


def tags_list(active_ids, current_id):
    return ','.join(str(i) for i in set(active_ids + [current_id]))


def blog_url(**kwargs):
    tag_ids = kwargs.get('tag')
    if tag_ids:
        return f"/tag/{tag_ids}"
    return "/blog"


class BlogTagController(http.Controller):

    @http.route(['/tag/<int:tag_id>', '/tag/<int:tag_id>/page/<int:page>'], type='http', auth='public', website=True)
    def blog_posts_by_tag(self, tag_id, page=1, **kwargs):
        BlogPost = request.env['blog.post'].sudo()
        domain = [('tag_ids', 'in', [tag_id])]
        sort_order = 'create_date desc'
        total = BlogPost.search_count(domain)

        pager = portal_pager(
            url=f'/tag/{tag_id}',
            total=total,
            page=page,
            step=10
        )

        posts = BlogPost.search(domain, order=sort_order, limit=10, offset=pager['offset'])
        tag = request.env['blog.tag'].sudo().browse(tag_id)

        return request.render('website_blog_tag_filter.blog_posts_by_tag', {
            'posts': posts,
            'pager': pager,
            'tag': tag,
            'page_name': 'blog_tag_page',
            'active_tag_ids': [tag_id],
            'tags_list': tags_list,
            'blog_url': blog_url,
            'search_count': total,  # Lisää tämä
        })
