{
    'name': 'Matter Reports',
    'version': '13.0.0.0.1',
    'summary': 'Matter Custom Reports',
    'description': 'Matter Custom Reports',
    'category': 'Reports',
    'author': 'JUMO Technologies',
    'website': 'https://www.jumotech.com',
    'license': '',
    'depends': ['account', 'matter_sale'],
    'data': [
        'reports/account_invoice.xml',
        'reports/sale_order.xml',
        'reports/purchase_order.xml',
    ],
    'installable': True,
    'auto_install': False
}
