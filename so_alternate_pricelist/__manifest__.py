# -*- coding: utf-8 -*-
{
    'name': "Sale Order Alternate PriceList",
    'summary': "Sale Order Atlernate PriceList",
    'description': """
Customization in order to add an alternate pricelist on a sale order that will be taken into account for generating reports""",
    'author': "Odoo SA",
    'website': "https://www.odoo.com",
    'category': 'Report',
    'version': '1.0',
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
