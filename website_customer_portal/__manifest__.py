{
    "name": "Customer Portal",
    "summary": """Matter Customer Portal""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Babatope Ajepe",
    "website": "http://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "1.7",
    "depends": [
        "base",
        "website",
        "portal",
        "sale_crm",
        "purchase",
        "pol_on_so",
        "sale_stock",
        "purchase_stock",
        "sale_management",
        "website_enterprise",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/crm_lead.xml",
        "views/sale_order.xml",
        "views/assets.xml",
        "views/portal.xml",
        "views/purchase_order.xml",
    ],
}
