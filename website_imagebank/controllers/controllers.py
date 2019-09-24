from odoo import http, _, tools
import base64
from PIL import Image, ExifTags
from io import BytesIO
import traceback

class VisitorImgUpload(http.Controller):

    def fix_img_orientation(self, img, exif):
        try:
            if exif:
                orientation = dict(img._getexif().items())[274]
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except Exception as e:
            print(e)
        return img

    def compress_image(self, image):
        img = Image.open(BytesIO(image))
        if 'exif' in img.info:
            exif = img.info['exif']
        else:
            exif = False

        opt = dict(format=img.format or format)
        if img.format == 'PNG':
            opt.update(optimize=True)
            if img.mode != 'P':
                img = img.convert('RGBA').convert('P', palette=Image.WEB, colors=256)

        elif img.format == 'JPEG':
            opt.update(optimize=True, quality=80)

        img_save = BytesIO()

        img = self.fix_img_orientation(img, exif)

        img.save(img_save, **opt)
        return img_save.getvalue()

    #return tools.image_save_for_web(img)

    @http.route('/imagebank', auth='public', type='http', website=True)
    def visitor_gallery(self, **kw):
        categories = http.request.env['imagebank.image'].get_category_list()
        image_urls = http.request.env['imagebank.image'].get_published_urls()
        image_urls_by_category = \
            http.request.env['imagebank.image'].get_image_urls_by_category()
        return http.request.render('website_imagebank.imagebank_gallery', {
            'categories': categories,
            'image_urls': image_urls,
            'image_urls_by_category': image_urls_by_category,
        })

    @http.route(['/imagebank/add_image'], type='http', auth='public', methods=['POST'], website=True)
    def create_slide(self, *args, **post):
        if post.get('image'):
            try:
                for img_filestorage in http.request.httprequest.files.getlist('image'):

                    Attachment = http.request.env['ir.attachment'].sudo()
                    VisitorImage = http.request.env['imagebank.image'].sudo()

                    img = img_filestorage.read()
                    filename = img_filestorage.filename
                    datas = base64.b64encode(img)
                    img_compressed = self.compress_image(img)
                    datas_compressed = base64.b64encode(img_compressed)
                    category = http.request.env['imagebank.category'].search(
                        [('name', '=', post.get('category'))])

                    attachment = Attachment.create({
                        'name': filename,
                        'datas': datas_compressed,
                        'type': 'binary',
                        'datas_fname': filename,
                        'public': True,
                    })

                    VisitorImage.create({
                        'name': filename,
                        'filename': filename,
                        'attachment': attachment.id,
                        'image_url': "/web/image/" + str(attachment.id) + "/" + filename,
                        'category': category.id,
                    })

                return http.request.render('website_imagebank.imagebank_gallery_thank_you', {})
            except Exception as e:
                traceback.print_exc()
                print(e)
                return http.request.render('website_imagebank.imagebank_gallery_error', {
                    'message': ""
                })

            else:
                return http.request.render('website_imagebank.imagebank_gallery_error', {
                    'message': _('Image file missign.')
                })



