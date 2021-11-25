# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_purchase_order_lines(self):
        for rec in self:
            rec['po_line_ids'] = rec.picking_ids.mapped(
                'move_lines.move_orig_ids.picking_id.purchase_id.order_line')

    # Migrated from field_sale_order__x_po_line_ids
    po_line_ids = fields.One2many('purchase.order.line', 'so_id', string='Purchase Order Lines', compute=_compute_purchase_order_lines)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_purchase_order_lines(self):
        for rec in self:
            rec['po_line_ids'] = rec.order_id.po_line_ids.filtered(
                lambda pol, rec=rec: pol.product_id == rec.product_id)

    def _compute_po_line_ok(self):
        for rec in self:
            rec['po_line_ok'] = sum(rec.po_line_ids.mapped('product_qty') or []) >= rec.product_uom_qty

    # Migrated from field_sale_order_line__x_po_line_ids
    po_line_ids = fields.One2many('purchase.order.line', 'so_line_id', string='Purchase Order Lines', compute=_compute_purchase_order_lines)

    # Migrated from field_sale_order_line__x_po_line_ok
    po_line_ok = fields.Boolean(string='Purchase Line OK', compute=_compute_po_line_ok)

