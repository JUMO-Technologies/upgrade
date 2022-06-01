from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_stock_old = fields.Boolean(string="In stock for 15 days", compute="_compute_is_stock_old", store=True)

    @api.depends("stock_move_ids")
    def _compute_is_stock_old(self):
        days15date = fields.Datetime.subtract(fields.Datetime.now(), days=15)
        for product in self:
            product.is_stock_old = product._get_is_stock_old(days15date)

    def _get_is_stock_old(self, days15date):
        self.ensure_one()
        if self.qty_available > 0:
            qty = self.qty_available
            for prod_move in self.env['stock.move.line'].search([('product_id', '=', self.id),
                                                                 ('picking_id.picking_type_id.code', '=', 'incoming'),
                                                                 ('state', '=', 'done')],
                                                                order="date desc"):
                if qty <= 0:
                    break
                qty -= prod_move.qty_done
                if prod_move.date <= days15date:
                    return True
        return False
