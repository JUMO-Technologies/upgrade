# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    linked_original_so_id = fields.Many2one('sale.order', string='Original Sale Order', index=True, copy=False)
    linked_so_ids = fields.One2many('sale.order', 'linked_original_so_id', string='Linked Sale Order', index=True, copy=False)

