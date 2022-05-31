from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one("sale.order", compute="_compute_sale_order_source", store=True)
    sale_count = fields.Integer(compute="_compute_sale_order_source", store=True)
    sale_team_id = fields.Many2one(related="sale_order_id.team_id")
    sale_user_id = fields.Many2one(related="sale_order_id.user_id", string="User SO")

    @api.depends('origin')
    def _compute_sale_order_source(self):
        for order in self:
            sale_order = self.env['sale.order'].search([('name', '=', order.origin)], limit=1)
            order.sale_order_id = sale_order or False
            order.sale_count = sale_order and 1 or 0

    def view_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
            'res_model': "sale.order",
        }

    @api.onchange("group_id")
    def _onchange_group_id(self):
        return {'value': {"origin": self.group_id and self.group_id.name or ""}}

    @api.onchange("sale_order_id")
    def _onchange_sale_order_id(self):
        pick_type_sale = False
        if self.sale_order_id:
            pick_type_sale = self.env['stock.picking.type'].search([
                ('code', '=', "incoming"), ("warehouse_id", "=", self.sale_order_id.warehouse_id.id)
            ], limit=1)
        return {'value': {"picking_type_id": pick_type_sale or self.picking_type_id}}

    @api.constrains("sale_order_id", "picking_type_id")
    def _constrains_picking_type_id(self):
        for order in self:
            if order.sale_order_id and order.sale_order_id.warehouse_id.id != order.picking_type_id.warehouse_id.id and \
                    order.date_order > "2022-05-31":
                raise ValidationError(_("Sorry it can not be choose this picking type for this sale team"))
