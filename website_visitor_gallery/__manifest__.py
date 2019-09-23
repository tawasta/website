{
    'name': "Website Visitor Gallery",
    'summary': """
Allow website visitors to upload images to website visitor gallery.
    """,
    'description': """
- Allow website visitors to upload pictures
- Curate pictures before publishing
    """,
    'website': 'http://www.tawasta.fi',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'category': 'Website',
    'version': '10.0.1.0.0',
    'depends': [
        'website',
        'website_form_recaptcha',
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
