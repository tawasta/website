{
    'name': "website_gallery_mobile_fix",
    'summary': "Fixes odoo website gallery mobile view",
    'description': """
        - Fix images having nospace between in gallery grid mode in mobile""",
    'author': 'Oy Tawasta OS Technologies Ltd.',
    'license': 'AGPL-3',
    'website': 'http://www.tawasta.fi',
    'category': 'Website',
    'version': '10.0.1.0.0',
    'depends': [
        'website',
    ],
    'data': [
        'views/assets_frontend.xml',
    ],
    'demo': [],
}
