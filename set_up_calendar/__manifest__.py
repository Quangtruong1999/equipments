# -*- coding: utf-8 -*-
{
    'name': "Đăng ký sử dụng thiết bị",
    'summary': """
        Quản lý, đặt lich sử dụng các thiết bị văn phòng""",

    'description': """
        Quản lý, đặt lich sử dụng các thiết bị văn phòng
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/calendar_event_views.xml',
        'views/equipment_tag_views.xml',
        'views/equipment_manager_views.xml',
        'views/booking_history_views.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
