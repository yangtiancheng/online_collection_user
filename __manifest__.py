# -*- coding: utf-8 -*-
{
    'name': "Collection User Information Module",

    'summary': """Collection User Information""",

    'description': """Collection User Information""",

    'author': "YTC",
    'website': "https://www.yangtiancheng.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Common',
    'version': '1.0',
    'sequence': 1,

    # any module necessary for this one to work correctly
    'depends': ['mail',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/collection_user_info.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
        "static/src/xml/*.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}