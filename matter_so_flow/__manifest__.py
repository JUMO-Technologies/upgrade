# -*- coding: utf-8 -*-
{
    'name': "matter_so_flow",

    'summary': """
         Modifications in the Sale Order/Quotation's step - Not on the report""",

    'description': """
        Task id: 1869235

        1. When he creates a sale order and the quantity ordered is higher that the quantity that he has in forecasted quantity ( WH1 + WH2) then he can't validate the Sale Order. He wants to have a blocked message saying : you don't have enough stock , you can not validate your sale order.

        2. He would like to see in the Sale Order/Quotation how many units of a product ( forecasted quantity) he has  in his Warehouse 1 = ( Warehouse where the goods are salable).

        3. He would like to have the possibility to duplicate a line on the sale order/quotation.
    """,

    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",

    'category': 'Customization',
    'version': '13.0.1.1',
    'depends': ['sale', 'stock'],

    'data': [
        'views/so_line_forecast.xml',
    ],
}
