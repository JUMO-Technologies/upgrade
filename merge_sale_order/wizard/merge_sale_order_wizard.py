# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class MergePurchaseOrder(models.TransientModel):
    _name = 'merge.sale.order'
    _description = 'Merge Purchase Order'

    merge_type = fields.Selection([
            ('new_cancel',
                'Create new order and cancel all selected sale orders'),
            ('merge_cancel',
             'Merge order on existing selected order and cancel others'),
        ], default='new_cancel')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.onchange('merge_type')
    def onchange_merge_type(self):
        res = {}
        for order in self:
            order.sale_order_id = False
            if order.merge_type in ['merge_cancel', 'merge_delete']:
                sale_orders = self.env['sale.order'].browse(
                    self._context.get('active_ids', []))
                res['domain'] = {
                    'sale_order_id':
                    [('id', 'in',
                        [sale.id for sale in sale_orders])]
                }
            return res

    def merge_orders(self):
        sale_orders = self.env['sale.order'].browse(
            self._context.get('active_ids', []))
        existing_so_line = False
        if len(self._context.get('active_ids', [])) < 2:
            raise UserError(
                _('Please select atleast two sale orders to perform '
                    'the Merge Operation.'))
        partner = sale_orders[0].partner_id.id
        if any(order.partner_id.id != partner for order in sale_orders):
            raise UserError(
                _('Please select Sale orders whose Customers are same to '
                    ' perform the Merge Operation.'))
        lead = sale_orders[0].lead_id.id
        if any(order.lead_id.id != lead for order in sale_orders):
            raise UserError(
                _('Please select Sale orders whose Leads are same to '
                    ' perform the Merge Operation.'))
        if self.merge_type == 'new_cancel':
            so = self.env['sale.order'].with_context({
                'trigger_onchange': True,
                'onchange_fields_to_trigger': [partner]
            }).create({'partner_id': partner, 'lead_id': lead})
        elif self.merge_type == 'merge_cancel':
            so = self.sale_order_id
        default = {'order_id': so.id}
        last_sequence = so.order_line and so.order_line[-1].sequence or 0
        for order in sale_orders:
            if order == so:
                continue
            if order.order_line:
                last_sequence += 10
                so.write({'order_line': [
                    (0, 0, dict(default, **{
                        'display_type': 'line_section',
                        'name': order.name,
                        'sequence': last_sequence,
                    }))]}
                )
            for line in order.order_line:
                last_sequence += 10
                line.copy(default=dict(default, **{'sequence': last_sequence}))
        for order in sale_orders:
            if order != so:
                order.sudo().action_cancel()
