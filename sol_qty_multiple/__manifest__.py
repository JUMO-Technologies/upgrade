# -*- coding: utf-8 -*-
{
    'name': "sol qty multiple",
    'description': """
Add a button on a sale order to adjust the quantity of a product on sale order lines,
depending on the multiple defined on the product related to the line
    """,
    'author': "Odoo SA",
    'depends': [
        'website_sale',
    ],
    'version': '13.0.1.1',
    'data': [
        'security/security.xml',
        'views/product.xml',
        'views/sale_order.xml',
    ],
}