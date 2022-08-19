{
    'name': 'Matter Reports',
    'version': '15.0.1.1.0',
    'summary': 'Matter Custom Reports',
    'category': 'Reports',
    'author': 'JUMO Technologies S.L.',
    'website': 'https://www.jumotech.com',
    'license': 'LGPL-3',
    'depends': ['account', 'matter_sale'],
    'data': [
        'reports/account_invoice.xml',
        'reports/sale_order.xml',
        'reports/purchase_order.xml',
    ],
    'installable': True,
    'auto_install': False
}
