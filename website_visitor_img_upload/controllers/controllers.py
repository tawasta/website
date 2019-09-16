from odoo import http
import base64

class VisitorImgUpload(http.Controller):
    @http.route('/visitor_gallery/image', auth='public', type='http', website=True)
    def visitor_gallery_image(self, **kw):
        return http.request.render('website_visitor_img_upload.visitor_gallery', {})

    @http.route('/visitor_gallery', auth='public', type='http', website=True)
    def visitor_gallery(self, **kw):
        images = http.request.env['visitor.image'].get_published()
        return http.request.render('website_visitor_img_upload.visitor_gallery', {
            'images': images
        })

    @http.route(['/visitor_gallery/add_image'], type='http', auth='public', methods=['POST'], website=True)
    def create_slide(self, *args, **post):
        if post.get('image'):
            attach = post.get('image').stream
            f = attach.getvalue()
            f = base64.b64encode(f)
            vals = {
                'image': f
            }
            try:
                http.request.env['visitor.image'].create(vals)
            except Exception as e:
                print("ERROR:")
                print(e)

            return http.request.render('website_visitor_img_upload.visitor_gallery', {})
        else:
            return http.request.render('website_visitor_img_upload.visitor_gallery', {})



