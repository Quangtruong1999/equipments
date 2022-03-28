# -*- coding: utf-8 -*-
{
    'name': "Booking Equipment",

    'summary': """
        Quản lý, đặt lich sử dụng các thiết bị văn phòng""",

    'description': """
        Quản lý, đặt lich sử dụng các thiết bị văn phòng
    """,

    'author': "CLOUDMEDIA CO.,LTD",
    'website': "https://cloudmedia.vn/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/equipment_tag_views.xml',
        # 'views/equipment_manager_views.xml',
        # 'views/register_equipment_views.xml',
        # 'views/booking_history_views.xml',
        # 'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
