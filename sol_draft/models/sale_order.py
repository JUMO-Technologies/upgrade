# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.product_id.generic')
    def _compute_generic(self):
        for rec in self:
            rec.generic = max(rec.order_line.mapped('product_id.generic') or [False])

    # Migrated from x_generic (sol_draft.field_sale_order__x_generic)
    generic = fields.Boolean('Generic', compute=_compute_generic)

    # Migrated from x_draft (sol_draft.field_sale_order__x_draft)
    draft = fields.Boolean('Draft')

    # Migrated from x_draft_so_id (sol_draft.field_sale_order__x_draft_so_id)
    draft_so_id = fields.Many2one('sale.order', string='Draft SO')

    # Migrated from x_draft_so_line_ids (sol_draft.field_sale_order__x_draft_so_line_ids)
    draft_so_line_ids = fields.One2many('sale.order.line', 'draft_order_id', string='Draft Lines')

    def action_open_form_simple_line(self):
        """ Open simple form view that allows to swap SOL from standard to draft
        :return:
        """
        self.ensure_one()
        view_id = self.env.ref('sol_draft.view_sale_order_form_simple_line').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Form Simple Line',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'sale.order',
            'view_id': view_id,
            'res_id': self.id,
            'context': self.env.context,
            'target': 'new',
    }

    def action_open_form_simple_draft_line(self):
        """ Open simple form view that allows to swap SOL from draft to standard
        :return:
        """
        self.ensure_one()
        view_id = self.env.ref('sol_draft.view_sale_order_form_simple_draft_line').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Form Simple Draft Line',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'sale.order',
            'view_id': view_id,
            'res_id': self.id,
            'context': self.env.context,
            'target': 'new',
        }

    def action_sol_standard2draft(self):
        """ Move the SOL's from the main SO to a duplicated draft SO
        :return:
        """
        for rec in self:
            rec.order_line.standard2draft()

    def action_sol_draft2standard(self):
        """
        Move the SOL's from the duplicated draft SO to the main SO
        // TODO For now, nothing is planned for the draft SO, they just stay in the system, invisible with the ir.rule
        // Maybe it could be deleted here, if all SOL swapped to standard ?
        :return:
        """
        for rec in self:
            rec.draft_so_line_ids.draft2standard()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Migrated from x_draft_order_id (sol_draft.field_sale_order_line__x_draft_order_id)
    draft_order_id = fields.Many2one('sale.order', string='Draft SO')

    # Migrated from x_swap (sol_draft.field_sale_order_line__x_swap)
    swap = fields.Boolean('Swap')

    def standard2draft(self):
        """
        Move the SOL from the main SO to a duplicated draft SO
        :return:
        """

        def duplicate(so):
            draft_so = so.copy(default={
                'draft': True,
                'order_line': False,
            })
            so.write({
                'draft_so_id': draft_so.id,
            })
        for rec in self:
            if not rec.swap or rec.draft_order_id:
                continue
            so = rec.order_id
            if so.state not in ['draft', 'sent']:
                continue
            if not so.draft_so_id:
                duplicate(so)
            rec.order_id = so.draft_so_id.id
            rec.draft_order_id = so.id
            rec.swap = False

    def draft2standard(self):
        """
        Move the SOL from the duplicated draft SO to the main SO
        :return:
        """
        for rec in self:
            if not rec.swap or not rec.draft_order_id:
                continue
            so = rec.draft_order_id
            if so.state not in ['draft', 'sent'] and rec.product_id.generic:
                continue
            rec.order_id = so.id
            rec.draft_order_id = False
            rec.swap = False
            if rec.state == 'sale':
                rec._action_procurement_create()
