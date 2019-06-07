{
    'name': "website_filebank",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '12.0.1.0.0',
    'depends': [
        'website_slides',
    ],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'data/filebank.xml',
    ],
    'demo': [],
}
