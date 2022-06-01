from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    display_discount1 = fields.Boolean(compute="_compute_total_discount")
    display_discount2 = fields.Boolean(compute="_compute_total_discount")

    @api.depends("invoice_line_ids")
    def _compute_total_discount(self):
        for invoice in self:
            invoice.display_discount1 = any(invoice.invoice_line_ids.mapped("discount1"))
            invoice.display_discount2 = any(invoice.invoice_line_ids.mapped("discount2"))


class AccountMoveline(models.Model):
    _inherit = "account.move.line"

    discount1 = fields.Float()
    discount1_store = fields.Float()
    discount2 = fields.Float()

    def _compute_discounts(self):
        for line in self:
            line.discount1 = line.discount1_store
            line.discount2 = (line.discount - line.discount1) / ((1 - line.discount1 / 100) or 1)

    @api.onchange("discount1", "discount2")
    def _onchange_discount(self):
        for line in self:
            line.discount1_store = line.discount1
            line.discount = line.discount1 + line.discount2 * (1 - line.discount1 / 100)

    @api.model
    def create(self, values):
        res = super(AccountMoveline, self).create(values)
        if res and (values.get("discount1_store", False) or values.get("discount", False)):
            res._compute_discounts()
        return res

    def write(self, values):
        res = super(AccountMoveline, self).write(values)
        if res and (values.get("discount1_store", False) or values.get("discount", False)):
            self._compute_discounts()
        return res
