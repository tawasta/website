from odoo import http
import base64

class VisitorImgUpload(http.Controller):
    @http.route('/visitor_gallery/image', auth='public', type='http', website=True)
    def visitor_gallery_image(self, **kw):
        return http.request.render('website_visitor_img_upload.visitor_gallery', {})

    @http.route('/visitor_gallery', auth='public', type='http', website=True)
    def visitor_gallery(self, **kw):
        image_urls = http.request.env['visitor.image'].get_published_urls()
        return http.request.render('website_visitor_img_upload.visitor_gallery', {
            'image_urls': image_urls
        })

    @http.route(['/visitor_gallery/add_image'], type='http', auth='public', methods=['POST'], website=True)
    def create_slide(self, *args, **post):
        if post.get('image'):
            Attachment = http.request.env['ir.attachment'].sudo()
            VisitorImage = http.request.env['visitor.image'].sudo()

            datas = base64.b64encode(post.get('image').read())
            filename = post.get('image').filename

            attachment = Attachment.create({
                'name': filename,
                'datas': datas,
                'type': 'binary',
                'datas_fname': filename,
                'public': True,
            })

            VisitorImage.create({
                'name': filename,
                'filename': post.get('image').filename,
                'attachment': attachment.id,
                'image_url': "/web/image/" + str(attachment.id) + "/" + filename,
            })
            return http.request.render('website_visitor_img_upload.visitor_gallery', {})
        else:
            return http.request.render('website_visitor_img_upload.visitor_gallery', {})



