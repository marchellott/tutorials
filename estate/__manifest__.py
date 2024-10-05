{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_properties_offer_form_views.xml',
        'views/estate_properties_offer_views.xml',
        'views/estate_property_type_form_views.xml',
        'views/estate_property_type_list_views.xml',
        'views/estate_properties_views_users.xml',
        'views/estate_property_view_kanban.xml',
        'views/estate_menus.xml',
        'views/estate_properties_list_views.xml',
        'views/estate_properties_form_views.xml',
        'views/estate_properties_search_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/css/custom_styles.css',
        ],
    },
    'license': 'LGPL-3',
}