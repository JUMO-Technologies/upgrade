from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount1 = fields.Float()
    discount1_store = fields.Float()
    discount2 = fields.Float()

    def _compute_discounts(self):
        for line in self:
            line.discount1 = line.discount1_store
            line.discount2 = (line.discount - line.discount1)/((1 - line.discount1 / 100) or 1)

    @api.onchange("discount1", "discount2")
    def _onchange_discount(self):
        for line in self:
            line.discount1_store = line.discount1
            line.discount = line.discount1 + line.discount2 * (1 - line.discount1 / 100)

    @api.model
    def create(self, values):
        res = super(SaleOrderLine, self).create(values)
        if res and (values.get("discount1_store", False) or values.get("discount", False)):
            res._compute_discounts()
        return res

    def write(self, values):
        res = super(SaleOrderLine, self).write(values)
        if res and (values.get("discount1_store", False) or values.get("discount", False)):
            self._compute_discounts()
        return res

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if res:
            res['discount1_store'] = self.discount1_store
        return res
