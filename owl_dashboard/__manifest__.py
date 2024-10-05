{
    'name' : 'Owl Dashboard',
    'version' : '1.0',
    'summary': 'OWL Dashboard',
    'sequence': -1,
    'description': """OWL Custom Dashboard""",
    'category': 'OWL',
    'depends' : ['base', 'web', 'sale', 'board'],
    'data': [
        'views/sales_dashboard.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_dashboard/static/src/components/**/*.js',
            'owl_dashboard/static/src/components/**/*.xml',
            'owl_dashboard/static/src/components/**/*.scss',
            'web/static/src/core/colors/colors.js',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js',
        ],
    },
}