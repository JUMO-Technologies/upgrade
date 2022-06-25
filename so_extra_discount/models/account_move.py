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
    discount2 = fields.Float()

    @api.onchange("discount1", "discount2")
    def _onchange_line_discount(self):
        for line in self:
            if line.exclude_from_invoice_tab:
                continue
            line.discount = line.discount1 + line.discount2 * (1 - line.discount1 / 100)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountMoveline, self).create(vals_list)
        if res and any(vls.get("discount", False) for vls in vals_list) and \
                not self._context.get("stop_iteration", False):
            res.with_context(stop_iteration=True)._onchange_line_discount()
        return res

    def write(self, values):
        res = super(AccountMoveline, self).write(values)
        if res and values.get("discount", False) and not self._context.get("stop_iteration", False):
            self.with_context(stop_iteration=True)._onchange_line_discount()
        return res
