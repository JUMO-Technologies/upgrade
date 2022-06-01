from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    late_payment = fields.Integer(compute="_compute_late_payment", search="_search_late_payment")
    programmed = fields.Boolean(string="Programmed")

    def _compute_late_payment(self):
        for move in self:
            today = fields.Date.today()
            days = ((move.invoice_date_due or today) - today).days
            move.late_payment = days

    def _search_late_payment(self, operator, value):
        today = fields.Date.today()
        late_pay = fields.Date.subtract(today, days=value)
        if operator == "<":
            operator = ">"
        elif operator == ">":
            operator = "<"
        return [('invoice_date_due', operator, late_pay)]
