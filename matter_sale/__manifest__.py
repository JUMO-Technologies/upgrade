{
    'name': 'Matter Sale',
    'version': '15.0.1.1.0',
    'summary': 'Custom Matter Sale Flow',
    'category': 'Sales',
    'author': 'JUMO Technologies S.L',
    'website': 'https://www.jumotech.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_quotation_builder',
        'sale_stock',
        'purchase_stock',
        'sale_purchase',
        'calendar',
        'website_sale'
    ],
    'data': [
        'views/crm_team.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
        'views/calendar_event.xml',
        'views/product.xml',
        'views/picking.xml',
    ],
    'installable': True,
    'auto_install': False
}
