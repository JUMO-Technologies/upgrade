# -*- coding: utf-8 -*-
{
    'name': "Automated Sequence",
    'description': """
Automated Sequence for product
    """,
    'author': "Odoo SA",
    'depends': [
        'sale_crm',
        'product',
        'sale_stock',
        'crm',
        'sol_qty_multiple',
    ],
    'version': '1.1',
    'data': [
        # Views
        'views/sale_order.xml',
        'views/sale_order_portal.xml',
        'views/product.xml',
        'views/lead.xml',

        # Security
        # Blocking users as they draft SO is in view
        # When upgrading to 13, I choose to use ir.rule instead of domains on act_window (which where not applied)
        # It seems to work correctly, but just needed sudo() to access them during the swaps
       
        #'security/ir.actions.act_window.csv',
        'security/ir_actions.xml',
    ],
}
