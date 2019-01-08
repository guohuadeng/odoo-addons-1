# -*- coding: utf-8 -*-
{
    'name': "delivery_kdniao",

    'summary': """
        快递鸟，快速解决您的客户物流跟踪及服务需求
    """,

    'description': """
        快递鸟功能  
        1.生成电子面单 
        2.取消电子面单
    """,

    'author': "黎伟杰",
    'website': "https://github.com/liweijie0812/odoo-addons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['delivery', 'company_city_extended'],

    # always loaded
    'data': [
        'views/delivery_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
