# -*- coding: utf-8 -*-
from odoo import fields, models


class SoDuplicateWizard(models.TransientModel):
    _name = 'so_duplicate_wizard'
    _description = 'Create accrual entry.'

    # migrated from so_duplicate_wizard_so_id_field
    so_id = fields.Many2one('sale.order', string='Original Sale Order', required=True, default=lambda self: self.env.context.get('active_id'))

    # migrated from so_duplicate_wizard_pricelist_id_field
    pricelist_id = fields.Many2one('product.pricelist', string='Price List', required=True)

    # migrated from so_duplicate_wizard_partner_id_field
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)

    # migrated from so_duplicate_wizard_server_action
    def action_duplicate(self):
        """ Duplicate a sale order & the lines and use the partner & pricelist from the wizard
        """
        self.ensure_one()
        new_so = self.so_id.copy({
            'pricelist_id': self.pricelist_id.id,
            'linked_original_so_id': self.so_id.id,
            'partner_id': self.partner_id.id,
        })
        # for line in self.so_id.order_line:
        #     line.copy({
        #         'order_id': new_so.id
        #     })
        #     line._onchange_discount()

            # so = self.env['sale.order'].create({
            #     'partner_id': self.partner_id.id,
            #     'pricelist_id': self.pricelist_id.id,
            #     'linked_original_so_id': self.so_id.id,
            #     'payment_term_id': self.so_id.payment_term_id.id,
            #     'user_id': self.so_id.user_id.id,
            #     'team_id': self.so_id.team_id.id,
            # })
            # for line in self.so_id.order_line:
            #     newline = self.env['sale.order.line'].create({
            #         'order_id': so.id,
            #         'product_id': line.product_id.id,
            #         'price_unit': line.price_unit,
            #         'product_uom_qty': line.product_uom_qty,
            #         'product_uom': line.product_uom,
            #         'name': line.name,
            #         'sequence': line.sequence,
            #     })
            #     # manually trigger the onchange on the discount
            #     newline._onchange_discount()
