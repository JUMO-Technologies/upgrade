from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirm_after_payment = fields.Boolean(string="Auto Confirm", default=False)
