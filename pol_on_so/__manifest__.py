# -*- coding: utf-8 -*-
{
    'name': "pol on so",
    'description': """
Show Purchase Order Lines related on SO
    """,
    'author': "Odoo SA",
    'version': '1.1',
    'depends': [
        'website_sale',
        'purchase',
        'stock',
    ],
    'data': [
        'views/sale_order.xml',
    ],
}