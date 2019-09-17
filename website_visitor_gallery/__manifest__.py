{
    'name': "Website Visitor Image Upload",
    'summary': """
Allow website visitors to upload images to website gallery.
    """,
    'description': """
    """,
    'website': 'http://www.tawasta.fi',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'category': 'Website',
    'version': '12.0.1.0.0',
    'depends': [
        'website',
        'website_gallery_mobile_fix',
    ],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'data/menu.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
}
