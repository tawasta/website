from odoo import http
from odoo.http import request, route
import json

class Example(http.Controller):
    @route('/example', auth='public')
    def state_example_handler(self):
        map_data = {
            'settings': {
                'zoom': 5,
                'center': {
                    'lat': 65.5274,
                    'lng': 27.1588
                }
            },
            'markers': [
                {
                    'position': {
                        'lat': 60.8701996,
                        'lng': 26.7018042,

                    },
                    'label': "A",
                    'show_infowindow': True,
                    'infowindow_open_start': False,
                    'infowindow_text': '<h5>Info</h5>'
                }
            ]
        }
        return json.dumps(map_data)
