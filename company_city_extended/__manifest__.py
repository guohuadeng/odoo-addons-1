# -*- coding: utf-8 -*-
{
    'name': "company_city_extended",

    'summary': """
        公司城市选择扩张为下拉框选择
    """,

    'description': """
        公司城市选择扩张为下拉框选择
    """,

    'author': "黎伟杰",
    'website': "https://github.com/liweijie0812/odoo-addons",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_cn_city'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}