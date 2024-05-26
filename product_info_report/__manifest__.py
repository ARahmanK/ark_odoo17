# -*- coding: utf-8 -*-
{
    'name': 'ARK Catalog Report',
    'version': '17.0',
    'category': 'Inventory',
    'summary': 'Generate Inventory Catalog Report',
    'description': '''
        1. Generate Inventory Catalog Report
    ''',
    'author': 'Abdul Rahman Khan',
    'website': 'https://www.fiverr.com/khan7438',
    'module_type': 'official',
    'depends': ['base','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_info_report_wizard.xml',
        'report/ir_actions_report.xml',
        'report/report.xml',
    ],
    'installable': True,
}

