from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    display_discount1 = fields.Boolean(compute="_compute_total_discount")
    display_discount2 = fields.Boolean(compute="_compute_total_discount")

    @api.depends("order_line")
    def _compute_total_discount(self):
        for order in self:
            order.display_discount1 = any(order.order_line.mapped("discount1"))
            order.display_discount2 = any(order.order_line.mapped("discount2"))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount1 = fields.Float()
    discount2 = fields.Float()

    @api.onchange("discount1", "discount2")
    def _onchange_discounts(self):
        for line in self:
            line.discount = line.discount1 + line.discount2 * (1 - line.discount1 / 100)

    @api.model
    def create(self, values):
        res = super(SaleOrderLine, self).create(values)
        if res and values.get("discount", False):
            res.with_context(stop_iteration=True)._onchange_discounts()
        return res

    def write(self, values):
        res = super(SaleOrderLine, self).write(values)
        if res and values.get("discount", False) and \
                not self._context.get("stop_iteration", False):
            self.with_context(stop_iteration=True)._onchange_discounts()
        return res

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if res:
            res['discount1'] = self.discount1
            res['discount2'] = self.discount2
        return res
