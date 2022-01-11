from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one("sale.order", compute="_compute_sale_order_source", store=True)
    sale_team_id = fields.Many2one(related="sale_order_id.team_id")
    sale_user_id = fields.Many2one(related="sale_order_id.user_id", string="User SO")

    @api.depends('origin')
    def _compute_sale_order_source(self):
        for order in self:
            sale_order = self.env['sale.order'].search([('name', '=', order.origin)], limit=1)
            order.sale_order_id = sale_order or False
