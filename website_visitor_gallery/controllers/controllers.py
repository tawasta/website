from odoo import http, _, tools
import base64
from PIL import Image
from io import BytesIO

class VisitorImgUpload(http.Controller):
    def optimize_img(self, img):
        img = Image.open(BytesIO(img))
        img_optimized = tools.image_save_for_web(img)
        return img_optimized

    @http.route('/visitor_gallery', auth='public', type='http', website=True)
    def visitor_gallery(self, **kw):
        image_urls = http.request.env['visitor.image'].get_published_urls()
        return http.request.render('website_visitor_gallery.visitor_gallery', {
            'image_urls': image_urls
        })

    @http.route(['/visitor_gallery/add_image'], type='http', auth='public', methods=['POST'], website=True)
    def create_slide(self, *args, **post):
        if post.get('image'):
            try:
                Attachment = http.request.env['ir.attachment'].sudo()
                VisitorImage = http.request.env['visitor.image'].sudo()

                img = post.get('image').read()
                img_optimized = self.optimize_img(img)
                datas = base64.b64encode(img_optimized)
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
                return http.request.render('website_visitor_gallery.visitor_gallery_thank_you', {})
            except Exception as e:
                print(e)
                return http.request.render('website_visitor_gallery.visitor_gallery_error', {
                    'message': ""
                })

        else:
            return http.request.render('website_visitor_gallery.visitor_gallery_error', {
                'message': _('Image file missign.')
            })



