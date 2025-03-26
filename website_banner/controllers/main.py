from odoo import http
from odoo.http import request
import base64

class AdvertisementController(http.Controller):

    @http.route(['/ad/render/<int:category_id>'], type='json', auth='public', website=True)
    def render_ad(self, category_id):
        """ Palauttaa satunnaisen mainoksen annetusta kategoriasta """
        ad = request.env['advertisement.advertisement'].sudo().get_random_ad(category_id)
        if ad:
            ad.increment_view()
            return {
                'image': f"/web/image/advertisement.advertisement/{ad.id}/image" if ad.image else "/web/static/img/placeholder.png",
                'url': f"/ad/click/{ad.id}",
                'title': ad.name
            }
        return {}

    @http.route(['/ad/click/<int:ad_id>'], type='http', auth='public', website=True)
    def ad_click(self, ad_id, **kwargs):
        """ Käsittelee mainoksen klikkauksen ja ohjaa käyttäjän oikeaan osoitteeseen """
        ad = request.env['advertisement.advertisement'].sudo().browse(ad_id)
        if ad.exists() and ad.is_active:
            ad.increment_click()
            return request.redirect(ad.url or '/')
        return request.redirect('/')
