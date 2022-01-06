{
    'name': 'Matter Sale',
    'version': '13.0.0.0.1',
    'summary': 'Custom Matter Sale Flow',
    'description': 'Custom Matter Sale Flow',
    'category': 'Sales',
    'author': 'JUMO Technologies',
    'website': '',
    'license': '',
    'depends': ['sale_quotation_builder', 'sale_stock', 'purchase_stock', 'sale_purchase'],
    'data': [
        'views/crm_team.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
    ],
    'installable': True,
    'auto_install': False
}
