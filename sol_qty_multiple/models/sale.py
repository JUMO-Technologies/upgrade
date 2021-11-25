# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_round_up_line_qty(self):
        self.order_line.round_up()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def round_up(self):
        """ Adjust the quantity of a product depending on the multiple defined on the product
        :return:
        """
        def is_almost_integer(val):
            values = []
            for digit in [-1, 0, 1]:
                values.append(abs(val - int(val) + digit))
            return min(values) < 0.000000000001
        for sol in self:
            multiple = sol.product_id.ce_product_m2box
            qty = sol.product_uom_qty

            if multiple or multiple and not is_almost_integer(qty / multiple):
                sol.product_uom_qty = int(qty / multiple + 1 - 0.000000000001) * multiple
            else:
                sol.product_uom_qty = sol.product_uom_qty
