{
    "name": "Sale Order Extra Discount",
    "version": "15.0.0.0.1",
    "summary": "Sale Order Extra Discount",
    "category": "Sales",
    "author": "JUMO Technologies S.L.",
    "website": "https://www.jumotech.com",
    "license": "LGPL-3",
    "depends": ["sale", "account"],
    "data": [
        "views/sale_order.xml",
        "views/account_move.xml",
        "reports/sale_order_reports.xml",
        "reports/report_invoice.xml",
    ],
    "post_init_hook": "_post_init_copy_discount",
    "installable": True,
    "auto_install": False
}
