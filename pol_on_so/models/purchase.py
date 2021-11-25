# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # migrated from field_sale_order__x_po_line_ids
    so_id = fields.Many2one('sale.order', string='Sale order')

    # migrated from field_sale_order_line__x_po_line_ids
    so_line_id = fields.Many2one('sale.order.line', string='Sale order line')

