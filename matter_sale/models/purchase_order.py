from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one("sale.order", compute="_compute_sale_order_source", store=True)
    sale_count = fields.Integer(compute="_compute_sale_order_source", store=True)
    sale_team_id = fields.Many2one("crm.team", compute="_compute_sale_team", store=True)
    sale_user_id = fields.Many2one(related="sale_order_id.user_id", string="User SO")
    invoiced_amount = fields.Monetary(string="Invoiced Amount", compute="_compute_invoiced_amount", store=True)

    @api.depends('origin')
    def _compute_sale_order_source(self):
        for order in self:
            sale_order = self.env['sale.order'].search([('name', '=', order.origin)], limit=1)
            order.sale_order_id = sale_order or False
            order.sale_count = sale_order and 1 or 0

    @api.depends("sale_order_id")
    def _compute_sale_team(self):
        for order in self:
            if order.sale_order_id:
                order.sale_team_id = order.sale_order_id.team_id
            else:
                order.sale_team_id = self.env['crm.team']._get_default_team_id(
                    user_id=order.create_uid.id
                )

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
                    order.date_order > datetime(day=2, month=6, year=2022):
                raise ValidationError(_("Sorry it can not be choose this picking type for this sale team"))
            elif order.sale_team_id and order.sale_team_id.warehouse_id.id != order.picking_type_id.warehouse_id.id and \
                    order.date_order > datetime(day=2, month=6, year=2022):
                raise ValidationError(_("Sorry it can not be choose this picking type for this sale team"))

    @api.depends("order_line.qty_invoiced", "order_line.price_unit")
    def _compute_invoiced_amount(self):
        for order in self:
            order.invoiced_amount = sum([l.qty_invoiced * l.price_unit for l in order.order_line])
