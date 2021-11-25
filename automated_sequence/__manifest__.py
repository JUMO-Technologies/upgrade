# -*- coding: utf-8 -*-
{
    'name': "Automated Sequence",
    'description': """
- Add product types related to an e-commerce category
- Have an automated sequence on a product type, automatically generated during creation
- Add an automated sequence on an e-commerce category, automatically generated during creation and based on the product type sequence
- Link an e-commerce category to a product, and init the internal reference of the product with the sequence related to the e-commerce category
    """,
    'author': "Odoo SA",
    'depends': [
        'website_sale',
    ],
    'version': '13.0.1.1',
    'data': [
        'security/ir.model.access.csv',
    ],
}
