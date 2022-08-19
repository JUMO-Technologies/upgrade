# -*- coding: utf-8 -*-
{
    'name': "Alanta Payment Term",
    'author': "Odoo SA",
    'version': '15.0.1.1.0',
    'depends': [
        'sale',
        'purchase',
        'account',
    ],
    'data': [
        # Views
        'views/payment_term.xml',
        'views/account_invoice.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',

        # Reports
        'reports/account_invoice.xml',
        'reports/sale_order.xml',

        # One time fix
        'actions/fix.xml',
    ],
}
