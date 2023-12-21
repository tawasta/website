from odoo import http
from odoo.http import request, content_disposition
import base64

class SlideDownloadController(http.Controller):
    @http.route('/slides/slide/download/<model("slide.slide"):slide>/', auth='public')
    def download_slide(self, slide, **kwargs):
        if slide.datas:
            # Dekoodaa binääridata base64-muodosta
            data = base64.b64decode(slide.datas)

            # Määritä oikea sisältötyyppi
            content_type = 'image/jpeg' if slide.mime_type == 'image/jpeg' else 'image/png'
            filename = '{}.{}'.format(slide.name, 'jpg' if slide.mime_type == 'image/jpeg' else 'png')

            return request.make_response(data,
                                         [('Content-Type', content_type),
                                          ('Content-Disposition', content_disposition(filename))])
        return request.not_found()
