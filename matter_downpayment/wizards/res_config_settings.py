from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    account_downpayment_supplier_id = fields.Many2one(related="company_id.account_downpayment_supplier_id",
                                                      readonly=False)
