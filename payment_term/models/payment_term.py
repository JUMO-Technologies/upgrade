from odoo import api, fields, models


class PaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    special_term = fields.Boolean(string='Special Term')
    number_days = fields.Integer(string='Number of Days')
    day_month = fields.Integer(string='Day of Month')
