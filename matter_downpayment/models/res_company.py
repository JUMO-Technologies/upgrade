from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    account_downpayment_supplier_id = fields.Many2one("account.account", string="Supplier Downpayment Account")
