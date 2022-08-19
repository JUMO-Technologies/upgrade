{
    'name': 'Supplier Validation',
    'version': '15.0.0.0.1',
    'summary': 'Custom supplier fields',
    'category': 'Partner',
    'author': 'Jumo Technologies S.L.',
    'website': 'https://www.jumotech.com',
    'license': 'LGPL-3',
    'depends': ['base', 'stock'],
    'data': [
        'views/res_partner.xml',
        'reports/stock_picking.xml',
    ],
    'installable': True,
    'auto_install': False
}
