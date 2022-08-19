# -*- coding: utf-8 -*-
{
    'name': "Sale Order Alternate PriceList",
    'summary': "Sale Order Atlernate PriceList",
    'author': "Odoo SA",
    'website': "https://www.odoo.com",
    'category': 'Report',
    'version': '15.0.1.0.0',
    'depends': [
        'base',
        'base_automation',
        'sale'
    ],
    'data': [
        'security/security.xml',
        'wizard/so_wizard.xml',
        'views/so_views.xml',
    ],
    'demo': [],
    'installable': True,
}
