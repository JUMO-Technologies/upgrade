{
    "name": "Crm Matter",
    "summary": """
        Sort crm kanban view based on the next activity deadline
        """,
    "category": "",
    "version": "13.0.1.0.1",
    "author": "Odoo PS",
    "website": "http://www.odoo.com",
    "license": "OEEL-1",
    "depends": ['crm', 'account_bank_statement_import_camt'],
    "data": [
        "views/crm_lead.xml",
    ],

    # Only used to link to the analysis / Ps-tech store
    "task_id": [2439202],
}
