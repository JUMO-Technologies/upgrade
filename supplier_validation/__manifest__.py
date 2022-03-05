{
    'name': 'Supplier Validation',
    'version': '13.0.0.0.1',
    'summary': 'Custom supplier fields',
    'description': 'Custom supplier fields',
    'category': 'Partner',
    'author': 'Jumo Technologies',
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
