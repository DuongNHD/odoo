# -*- coding: utf-8 -*-
{
    'name': "Fonality Integration",

    'summary': """
        Fonality Integration
    """,

    'description': """
        Fonality Integration
    """,

    'author': "Bennie-duongnhbennie@gmail.com",
    'website': "",
    'images': ['images/fonality_account.jpeg', 'images/fonality_configure.jpeg', 'images/button_call.jpeg'],

    'category': 'Tools',
    'version': '0.1',
    'depends': ['base','web'],

    'data': [
        #'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_users_view.xml',
        'views/config_view.xml',
        'views/test_call_view.xml',
        'views/simple_dialog.xml',
        'views/partner_form.xml',
        'views/call_history_view.xml',
        'views/menu.xml',

        'data/config.xml',

        'views/assets.xml',
    ],

    'qweb': ['static/src/xml/*.xml'],
    'currency': 'EUR',
    'price': 250,
}
