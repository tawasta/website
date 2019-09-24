from odoo import http, _, tools
import base64
from PIL import Image, ExifTags
from io import BytesIO

class VisitorImgUpload(http.Controller):

    def compress_image(self, image):
        """
        Function to compress image accordingly.
                    This function uses image_save_for_web-utility from tools.
                        Max dimensions can be set on system parameters.
                            Process of compressing image:
                                    - Calculate new image dimensions according to MAX_WIDTH and MAX_HEIGHT
                                        - Resize image with new dimensions
                                            - Compress using image_save_for_web -utility

        :param image: Image data in binary
            :return: Compressed and resized image data in binary
        """
        #max_width_key = 'website_skills_qualification.image_max_width'
        #max_height_key = 'website_skills_qualification.image_max_height'
        MAX_WIDTH = 1024 #int(http.request.env['ir.config_parameter'].sudo().get_param(max_width_key))
        MAX_HEIGHT = 1024 #int(http.request.env['ir.config_parameter'].sudo().get_param(max_height_key))
        img = Image.open(BytesIO(image))
        if 'exif' in img.info:
            exif = img.info['exif']
        else:
            exif = False
        (width, height) = img.size
        #_logger.debug("Image starting size: (%s, %s)" % (width, height))
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            if width > height:
                if width > MAX_WIDTH:
                    new_height = int(round((MAX_WIDTH / float(width)) * height))
                    new_width = MAX_WIDTH
            else:
                if height > MAX_HEIGHT:
                    new_width = int(round((MAX_HEIGHT / float(height)) * width))
                    new_height = MAX_HEIGHT
            img.thumbnail((new_width, new_height), Image.ANTIALIAS)
            #_logger.debug("Compressed size: (%s, %s)" % (new_width, new_height))

        opt = dict(format=img.format or format)
        if img.format == 'PNG':
            opt.update(optimize=True)
            if img.mode != 'P':
                img = img.convert('RGBA').convert('P', palette=Image.WEB, colors=256)

        elif img.format == 'JPEG':
            opt.update(optimize=True, quality=80)


        img_save = BytesIO()
        if exif:
            img.save(img_save, exif=exif, **opt)
        else:
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
                    datas_compressed = base64.b64encode(self.compress_image(img))
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
                print(e)
                return http.request.render('website_imagebank.imagebank_gallery_error', {
                    'message': ""
                })

            else:
                return http.request.render('website_imagebank.imagebank_gallery_error', {
                    'message': _('Image file missign.')
                })



